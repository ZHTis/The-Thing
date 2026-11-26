#!/usr/bin/env python3
"""Validate every canonical skill using skills-ref plus repository invariants.

Install requirements-validation.txt in a dedicated virtual environment first.
This checks packaging and references, not tool availability or task success.
"""
import argparse
import json
import re
from pathlib import Path
import yaml
from skills_ref import validate


def without_fenced_code(text):
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            token = match.group(1)[0]
            if fence is None:
                fence = token
            elif token == fence:
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def check(root):
    taxonomy = json.loads((root / "taxonomy.json").read_text())
    names = [name for group in taxonomy.values() for name in group["skills"]]
    if len(names) != len(set(names)):
        raise ValueError("[CAT001] Duplicate skill in taxonomy.json; list each skill once")
    classified = {name: key for key, group in taxonomy.items() for name in group["skills"]}
    paths = sorted(root.glob("*/SKILL.md")) + sorted((root / ".system").glob("*/SKILL.md"))
    results = []
    for entry in paths:
        errors = list(validate(entry.parent))
        text = entry.read_text()
        try:
            data = yaml.safe_load(text.split("---", 2)[1])
            if not isinstance(data, dict):
                raise ValueError("frontmatter must be a mapping")
        except (yaml.YAMLError, IndexError, ValueError) as exc:
            results.append({"name": entry.parent.name, "path": str(entry.parent.relative_to(root)),
                            "errors": errors + ["[SPEC001] Repair YAML frontmatter: " + str(exc)]})
            continue
        name = data.get("name")
        metadata = data.get("metadata", {})
        if not isinstance(metadata, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in metadata.items()):
            errors.append("[META001] metadata must map strings to strings; quote each value")
            metadata = {}
        if metadata.get("the-thing.category") != classified.get(name):
            errors.append("[CAT001] category does not match taxonomy.json; update metadata, taxonomy and index together")
        if len(text.splitlines()) >= 500:
            errors.append("[SIZE001] entrypoint exceeds repository limit of 499 lines; move details to references")
        if "/Users/" in text:
            errors.append("[PATH001] host-specific user path in entrypoint; move historical cases into references")
        if metadata.get("the-thing.invocation") == "explicit":
            policy_path = entry.parent / "agents/openai.yaml"
            try:
                config = yaml.safe_load(policy_path.read_text()) if policy_path.exists() else {}
                if not isinstance(config, dict):
                    config = {}
            except yaml.YAMLError:
                config = {}
            if config.get("policy", {}).get("allow_implicit_invocation") is not False:
                errors.append("[HOST001] explicit-only Codex host policy missing; set policy.allow_implicit_invocation to false")
        for link in re.findall(r"\]\(([^)]+)\)", without_fenced_code(text)):
            if link.startswith(("https://", "http://", "#", "/", "mailto:", "<")):
                continue
            target = link.split("#", 1)[0]
            if target and not (entry.parent / target).exists():
                errors.append("[LINK001] missing linked resource; supply the file or correct the relative path: " + target)
        results.append({"name": name, "path": str(entry.parent.relative_to(root)), "errors": errors})
    if set(classified) != {item["name"] for item in results}:
        raise ValueError("[CAT001] taxonomy does not cover exactly the installed canonical skills; update taxonomy.json")
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = check(args.root.resolve())
    failed = sum(bool(item["errors"]) for item in results)
    if args.json:
        print(json.dumps({"skills": results, "checked": len(results), "failed": failed}, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(("FAIL " if item["errors"] else "PASS ") + item["path"])
            for error in item["errors"]:
                print("  " + error)
        print(f"Checked {len(results)} skills; failed {failed}.")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
