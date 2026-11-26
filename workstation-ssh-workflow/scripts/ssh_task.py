#!/usr/bin/env python3
"""Preview or execute authorized Windows SSH steps with append-only JSONL audit output.

Python 3.10+ standard library and OpenSSH. Foreground tasks only. No shell=True,
eval, credential copying, Git resets, environment installation or retry loop.
"""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import subprocess
import threading
import time
import uuid


CREDENTIAL = re.compile(r"(?i)(?:password|api[_-]?key|access[_-]?token|secret)\s*[:=]\s*[^\s;]+|Bearer\s+\S+|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-[A-Za-z0-9_-]{30,}")
PRIVATE_START = re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----")
PRIVATE_END = re.compile(r"-----END (?:[A-Z]+ )?PRIVATE KEY-----")

LOG_MAX_BYTES = 20_000_000
LOG_TOTAL_FILES = 10


class AuditLog:
    """Single-writer, byte-bounded JSONL: active file plus nine archives."""
    def __init__(self, path, max_bytes=LOG_MAX_BYTES, total_files=LOG_TOTAL_FILES):
        self.path = Path(path)
        self.max_bytes = max_bytes
        self.total_files = total_files
        if max_bytes < 1 or total_files < 1:
            raise ValueError('Log limits must be positive')
        self.lock = None

    def __enter__(self):
        lock_path = self.path.with_name(self.path.name + '.lock')
        self.lock = os.fdopen(os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600), 'r+b')
        try:
            if os.name == 'nt':
                import msvcrt
                self.lock.seek(0)
                if not self.lock.read(1):
                    self.lock.write(b'0'); self.lock.flush()
                self.lock.seek(0)
                msvcrt.locking(self.lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.lock.close()
            raise OSError('Log already has an active writer; use a separate log path') from None
        return self

    def write(self, text):
        data = text.encode('utf-8')
        if len(data) > self.max_bytes:
            raise ValueError('Single audit event exceeds 20 MB; no truncation performed')
        size = self.path.stat().st_size if self.path.exists() else 0
        if size and size + len(data) > self.max_bytes:
            if size > self.max_bytes:
                raise ValueError('Existing log exceeds the limit; archive it separately before execution')
            oldest = self.path.with_name(self.path.name + '.' + str(self.total_files - 1))
            if self.total_files > 1:
                oldest.unlink(missing_ok=True)
                for n in range(self.total_files - 2, 0, -1):
                    src = self.path.with_name(self.path.name + '.' + str(n))
                    if src.exists():
                        src.replace(self.path.with_name(self.path.name + '.' + str(n + 1)))
                self.path.replace(self.path.with_name(self.path.name + '.1'))
            else:
                self.path.unlink()
        with os.fdopen(os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600), 'ab') as out:
            out.write(data)
            out.flush()

    def __exit__(self, *args):
        if self.lock:
            self.lock.close()


class Redactor:
    def __init__(self):
        self.private_key = False

    def clean(self, text):
        if self.private_key or PRIVATE_START.search(text):
            self.private_key = not bool(PRIVATE_END.search(text))
            return "[REDACTED PRIVATE KEY OUTPUT]\n"
        return CREDENTIAL.sub("[REDACTED CREDENTIAL]", text)


def ps_literal(text):
    return "'" + text.replace("'", "''") + "'"


def ensure_no_secrets(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in {"password", "token", "private_key", "api_key", "secret", "access_token", "authorization_header"}:
                raise ValueError("Credential fields do not belong in a task manifest")
            ensure_no_secrets(child)
    elif isinstance(value, list):
        for child in value:
            ensure_no_secrets(child)
    elif isinstance(value, str) and (CREDENTIAL.search(value) or PRIVATE_START.search(value)):
        raise ValueError("Credential-like material in manifest; use destination-owned authentication")


def validate_task(task):
    ensure_no_secrets(task)
    for key in ("task_id", "target", "steps", "log_file", "context", "authorization"):
        if key not in task:
            raise ValueError("Missing task field: " + key)
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", task["task_id"]):
        raise ValueError("task_id must be a short filename-safe identifier")
    if task.get("execution_mode", "foreground") != "foreground":
        raise ValueError("Runner supports foreground only; use an explicitly authorized durable-task mechanism separately")
    if not isinstance(task["authorization"], dict) or not task["authorization"].get("scope"):
        raise ValueError("Record the actual authorized scope; a manifest is not itself permission")
    if not isinstance(task["context"], dict) or any(k not in task["context"] for k in ("repository", "environment", "data")):
        raise ValueError("context must separately describe repository, environment and data readiness")
    target = task["target"]
    if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.@:-]*", target.get("ssh_target", "")):
        raise ValueError("Use a plain SSH alias or user@host without shell syntax or leading options")
    host = target.get("expected_hostname", "")
    if not isinstance(host, str) or not host or any(c in host for c in "\r\n"):
        raise ValueError("Record the expected Windows hostname before execution")
    if target.get("powershell", "powershell") not in {"powershell", "pwsh"}:
        raise ValueError("powershell must be powershell or pwsh")
    port = target.get("port", 22)
    if type(port) is not int or not 1 <= port <= 65535:
        raise ValueError("Invalid SSH port")
    if not isinstance(target.get("identity_file"), str) or not target["identity_file"]:
        raise ValueError("Specify an identity-file path, never private-key contents")
    timeout = task.get("timeout_seconds", 120)
    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or not 0 < timeout <= 86400:
        raise ValueError("timeout_seconds must be between 0 and 86400")
    if not isinstance(task["steps"], list) or not task["steps"]:
        raise ValueError("Provide at least one step")
    ids = set()
    for step in task["steps"]:
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", step.get("id", "")) or step["id"] in ids:
            raise ValueError("Step IDs must be unique filename-safe identifiers")
        ids.add(step["id"])
        script = step.get("script", "")
        if not isinstance(script, str) or not script.strip():
            raise ValueError("Every step needs a readable PowerShell script")
        if CREDENTIAL.search(script) or PRIVATE_START.search(script):
            raise ValueError("Credential-like material in script; authenticate on the destination, not inside logged commands")
        patterns = step.get("expect", [])
        if not isinstance(patterns, list) or not patterns or not all(isinstance(p, str) and p for p in patterns):
            raise ValueError("Every step needs non-empty output acceptance patterns")
        for pattern in patterns:
            re.compile(pattern)
    skill_root = Path(__file__).resolve().parents[1]
    for value in (task["log_file"],):
        path = Path(value).expanduser().resolve()
        if path.is_relative_to(skill_root):
            raise ValueError("Keep task manifests, logs and summaries outside the published skill folder")
    return task


def wrap_script(script, expected_host, marker):
    return f'''[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [Console]::OutputEncoding
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
function Invoke-CheckedNative {{
    param([string]$File, [string[]]$Arguments)
    & $File @Arguments
    if ($LASTEXITCODE -ne 0) {{ throw "Native command failed: $File; exit=$LASTEXITCODE" }}
}}
try {{
    Write-Output ({ps_literal(marker + 'HOST=')} + $env:COMPUTERNAME)
    if ($env:COMPUTERNAME -ine {ps_literal(expected_host)}) {{ throw 'Unexpected workstation hostname; task not started' }}
    $global:LASTEXITCODE = 0
    & {{
{script}
    }}
    if ($LASTEXITCODE -ne 0) {{ throw "Last native command failed: exit=$LASTEXITCODE" }}
    Write-Output {ps_literal(marker + 'DONE=0')}
    exit 0
}} catch {{
    [Console]::Error.WriteLine($_.ToString())
    exit 1
}}
'''


def command(task, step, marker):
    target = task["target"]
    source = wrap_script(step["script"], target["expected_hostname"], marker)
    encoded = base64.b64encode(source.encode("utf-16le")).decode("ascii")
    argv = ["ssh", "-T", "-i", str(Path(target["identity_file"]).expanduser()),
            "-p", str(target.get("port", 22)), "-o", "IdentitiesOnly=yes", "-o", "BatchMode=yes",
            "-o", "StrictHostKeyChecking=yes", "-o", "ConnectTimeout=10", "-o", "ServerAliveInterval=15",
            "-o", "ServerAliveCountMax=3", target["ssh_target"],
            target.get("powershell", "powershell") + " -NoProfile -NonInteractive -EncodedCommand " + encoded]
    return argv, source


def stop(proc):
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=3)


def run_step(task, step, emit, timeout):
    marker = "__SSH_AUDIT_" + uuid.uuid4().hex + "__"
    argv, source = command(task, step, marker)
    emit("command", step_id=step["id"], ssh_argv=argv[:-1], powershell=source,
         script_sha256=hashlib.sha256(source.encode("utf-8")).hexdigest(), transport="UTF-16LE/Base64 EncodedCommand")
    result = {"step_id": step["id"], "status": "unverified", "ssh_exit": None,
              "actual_hostname": None, "completion_marker": False, "missing_acceptance": [],
              "encoding_warning": False, "error_record_seen": False,
              "output_capture_complete": False, "capture_error": None}
    try:
        proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1)
    except OSError as exc:
        result.update(status="launch_failed", error=str(exc))
        emit("step_result", **result)
        return result
    messages = queue.Queue()
    def pump():
        try:
            for line in proc.stdout:
                messages.put(line)
        except (OSError, ValueError) as exc:
            messages.put(("capture_error", type(exc).__name__))
        finally:
            messages.put(None)
    worker = threading.Thread(target=pump, daemon=True)
    worker.start()
    deadline = time.monotonic() + timeout
    output = []
    redactor = Redactor()
    eof_received = False
    def consume(line):
        if isinstance(line, tuple):
            result["capture_error"] = line[1]
            emit("capture_error", step_id=step["id"], error_class=line[1])
            return
        if "\ufffd" in line:
            result["encoding_warning"] = True
        if re.search(r"<S\s+S=[\"']Error[\"']", line):
            result["error_record_seen"] = True
        clean = redactor.clean(line)
        emit("output", step_id=step["id"], stream="stdout+stderr", text=clean)
        output.append(clean)
        stripped = clean.strip()
        if stripped.startswith(marker + "HOST="):
            result["actual_hostname"] = stripped[len(marker + "HOST="):]
        if stripped == marker + "DONE=0":
            result["completion_marker"] = True
    try:
        while True:
            if time.monotonic() >= deadline:
                result["status"] = "timed_out"
                stop(proc)
                break
            try:
                line = messages.get(timeout=min(.1, max(.001, deadline - time.monotonic())))
            except queue.Empty:
                continue
            if line is None:
                eof_received = True
                proc.wait(timeout=max(.001, deadline - time.monotonic()))
                break
            consume(line)
    except subprocess.TimeoutExpired:
        result["status"] = "timed_out"
        stop(proc)
    except KeyboardInterrupt:
        result["status"] = "interrupted"
        stop(proc)
    finally:
        if proc.poll() is None:
            stop(proc)
        worker.join(timeout=1)
        # Keep termination output when available; bound draining so a stuck pipe
        # cannot pretend to finish or hang the caller indefinitely.
        drain_deadline = time.monotonic() + 1
        while time.monotonic() < drain_deadline:
            try:
                tail = messages.get_nowait()
            except queue.Empty:
                break
            if tail is None:
                eof_received = True
            else:
                consume(tail)
        result["output_capture_complete"] = eof_received and not worker.is_alive() and not result["capture_error"]
        if not worker.is_alive():
            proc.stdout.close()
    result["ssh_exit"] = proc.returncode
    joined = "".join(output)
    result["missing_acceptance"] = [p for p in step["expect"] if not re.search(p, joined, re.MULTILINE)]
    if result["status"] == "unverified":
        host_ok = (result["actual_hostname"] or "").casefold() == task["target"]["expected_hostname"].casefold()
        if (proc.returncode == 0 and host_ok and result["completion_marker"]
                and not result["missing_acceptance"] and not result["encoding_warning"]
                and not result["error_record_seen"] and result["output_capture_complete"]):
            result["status"] = "accepted"
        else:
            result["status"] = "failed_or_unverified"
    emit("step_result", **result)
    return result


def execute(task):
    validate_task(task)
    log_path = Path(task["log_file"]).expanduser().resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex
    results = []
    with AuditLog(log_path) as log:
        def emit(event, **fields):
            record = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "task_id": task["task_id"],
                      "run_id": run_id, "event": event, **fields}
            # All command/output events are mirrored; callers may separately tail this same JSONL.
            line = json.dumps(record, ensure_ascii=False)
            log.write(line + "\n")
            print(line, flush=True)
        emit("task_started", target=task["target"]["ssh_target"], expected_hostname=task["target"]["expected_hostname"],
             context=task["context"], authorization_scope=task["authorization"]["scope"])
        deadline = time.monotonic() + task.get("timeout_seconds", 120)
        for step in task["steps"]:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                result = {"step_id": step["id"], "status": "not_started_deadline", "ssh_exit": None}
                emit("step_result", **result)
            else:
                result = run_step(task, step, emit, remaining)
            results.append(result)
            if result["status"] != "accepted":
                break
        summary = {"task_id": task["task_id"], "run_id": run_id, "target": task["target"]["ssh_target"],
                   "status": "accepted" if len(results) == len(task["steps"]) and all(r["status"] == "accepted" for r in results) else "incomplete",
                   "steps": results, "not_started": [s["id"] for s in task["steps"][len(results):]],
                   "log_file": str(log_path), "context_claims": task["context"]}
        emit("task_result", **{k: v for k, v in summary.items() if k not in {"task_id", "run_id"}})
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path, help="Local, non-secret task manifest outside this skill folder")
    parser.add_argument("--execute", action="store_true", help="Run steps only after reviewing the manifest and existing user authorization")
    args = parser.parse_args()
    try:
        skill_root = Path(__file__).resolve().parents[1]
        if args.execute and args.task.resolve().is_relative_to(skill_root):
            raise ValueError("Copy the example manifest outside the public skill folder before configuring and executing it")
        task = validate_task(json.loads(args.task.read_text()))
        if not args.execute:
            for step in task["steps"]:
                argv, source = command(task, step, "PREVIEW__")
                print(json.dumps({"mode": "preview_only", "step_id": step["id"], "ssh_argv": argv[:-1], "powershell": source}, ensure_ascii=False))
            return 0
        result = execute(task)
        return 0 if result["status"] == "accepted" else 1
    except (OSError, ValueError, KeyError, TypeError, re.error) as exc:
        print(json.dumps({"status": "local_error", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
