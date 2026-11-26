import base64
from contextlib import redirect_stdout
import copy
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import ssh_task


class SSHTaskTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.task = {
            'task_id': 'fixture-001',
            'target': {'ssh_target': 'user@test-host', 'expected_hostname': 'TEST-HOST',
                       'identity_file': '~/.ssh/test_key'},
            'context': {key: {'status': 'unverified'} for key in ('repository', 'environment', 'data')},
            'authorization': {'scope': 'Offline fake transport fixture only'},
            'log_file': str(self.root / 'audit.jsonl'), 'timeout_seconds': 5,
            'steps': [{'id': 'query', 'script': "Write-Output 'QUERY_OK'", 'expect': ['QUERY_OK']}],
        }
        self.real_popen = subprocess.Popen

    def fake(self, mode='success'):
        def launch(argv, **kwargs):
            self.assertEqual(argv[0], 'ssh')
            self.assertNotIn('shell', kwargs)
            source = base64.b64decode(argv[-1].split()[-1]).decode('utf-16le')
            marker = re.search(r'(__SSH_AUDIT_[0-9a-f]+__)HOST=', source).group(1)
            lines = [marker + 'HOST=TEST-HOST', 'QUERY_OK', marker + 'DONE=0']
            rc = 0
            if mode == 'no-marker':
                lines = ['QUERY_OK']
            elif mode == 'wrong-host':
                lines[0] = marker + 'HOST=WRONG-HOST'
            elif mode == 'missing-output':
                lines[1] = 'OTHER_OUTPUT'
            elif mode == 'disconnect':
                lines = ['partial-output']; rc = 255
            elif mode == 'remote-error':
                lines = [marker + 'HOST=TEST-HOST', 'QUERY_OK']; rc = 1
            elif mode == 'clixml-error':
                lines.insert(1, '<Objs><S S="Error">nonterminating-error</S></Objs>')
            elif mode == 'redaction':
                lines[1:1] = ['password=hunter123', '-----BEGIN PRIVATE KEY-----', 'not-a-real-key', '-----END PRIVATE KEY-----']
            code = 'import sys,time\n'
            if mode == 'invalid-utf8':
                code += "sys.stdout.buffer.write(bytes([255, 10])); sys.stdout.flush()\n"
            for line in lines:
                code += 'print(' + repr(line) + ', flush=True)\n'
            code += "print('stderr-observation', file=sys.stderr, flush=True)\n"
            if mode == 'timeout-tail':
                code = "import signal,sys,time\ndef ended(*args):\n print('TERMINATION_TAIL',flush=True)\n sys.exit(0)\nsignal.signal(signal.SIGTERM,ended)\nprint('ready',flush=True)\ntime.sleep(5)\n"
            if mode == 'timeout':
                code = "import time\nprint('partial-output',flush=True)\ntime.sleep(5)\n"
            code += f'sys.exit({rc})\n'
            return self.real_popen([sys.executable, '-u', '-c', code], **kwargs)
        return launch

    def run_fake(self, mode='success'):
        with redirect_stdout(io.StringIO()), patch.object(ssh_task.subprocess, 'Popen', side_effect=self.fake(mode)) as mocked:
            result = ssh_task.execute(self.task)
        self.calls = mocked.call_count
        return result

    def events(self):
        return [json.loads(line) for line in Path(self.task['log_file']).read_text().splitlines()]

    def test_script_transport_preserves_dollar_quotes_and_chinese(self):
        script = "Get-ChildItem 'C:\\中文 文件' | ForEach-Object { $_.Name }\nWrite-Output 'it''s intact'"
        step = copy.deepcopy(self.task['steps'][0]); step['script'] = script
        argv, wrapped = ssh_task.command(self.task, step, 'TEST__')
        decoded = base64.b64decode(argv[-1].split()[-1]).decode('utf-16le')
        self.assertEqual(decoded, wrapped)
        self.assertIn(script, decoded)
        self.assertIn('StrictHostKeyChecking=yes', argv)
        self.assertIn('BatchMode=yes', argv)

    def test_success_requires_host_marker_and_acceptance(self):
        result = self.run_fake()
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(result['steps'][0]['ssh_exit'], 0)
        self.assertEqual(result['steps'][0]['actual_hostname'], 'TEST-HOST')
        self.assertTrue(any('stderr-observation' in e.get('text', '') for e in self.events()))

    def test_exit_zero_without_markers_is_not_success(self):
        self.assertEqual(self.run_fake('no-marker')['status'], 'incomplete')

    def test_wrong_host_is_not_accepted(self):
        self.assertEqual(self.run_fake('wrong-host')['status'], 'incomplete')

    def test_missing_acceptance_is_not_success(self):
        result = self.run_fake('missing-output')
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['steps'][0]['missing_acceptance'], ['QUERY_OK'])

    def test_disconnect_preserves_partial_failure_and_stops_followups(self):
        self.task['steps'].append({'id': 'next', 'script': 'Write-Output 2', 'expect': ['2']})
        result = self.run_fake('disconnect')
        self.assertEqual(self.calls, 1)
        self.assertEqual(result['steps'][0]['ssh_exit'], 255)
        self.assertEqual(result['not_started'], ['next'])
        self.assertIn('partial-output', Path(self.task['log_file']).read_text())

    def test_remote_error_even_with_matching_output_fails(self):
        self.assertEqual(self.run_fake('remote-error')['status'], 'incomplete')

    def test_timeout_is_incomplete(self):
        self.task['timeout_seconds'] = .1
        result = self.run_fake('timeout')
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['steps'][0]['status'], 'timed_out')

    def test_timeout_preserves_termination_tail_and_never_becomes_success(self):
        self.task['timeout_seconds'] = .2
        result = self.run_fake('timeout-tail')
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['steps'][0]['status'], 'timed_out')
        self.assertIn('TERMINATION_TAIL', Path(self.task['log_file']).read_text())
        self.assertTrue(result['steps'][0]['output_capture_complete'])

    def test_audit_is_append_only_and_has_distinct_run_ids(self):
        first = self.run_fake(); count = len(self.events())
        second = self.run_fake()
        self.assertGreater(len(self.events()), count)
        self.assertNotEqual(first['run_id'], second['run_id'])
        self.assertTrue(all(e['task_id'] == 'fixture-001' and e['timestamp_utc'] for e in self.events()))

    def test_output_credentials_and_multiline_key_are_redacted(self):
        self.assertEqual(self.run_fake('redaction')['status'], 'accepted')
        log = Path(self.task['log_file']).read_text()
        for raw in ('hunter123', 'not-a-real-key', 'BEGIN PRIVATE KEY'):
            self.assertNotIn(raw, log)
        self.assertIn('REDACTED', log)

    def test_invalid_utf8_does_not_get_silently_accepted(self):
        result = self.run_fake('invalid-utf8')
        self.assertEqual(result['status'], 'incomplete')
        self.assertTrue(result['steps'][0]['encoding_warning'])

    def test_clixml_error_record_cannot_hide_behind_exit_zero(self):
        result = self.run_fake('clixml-error')
        self.assertEqual(result['status'], 'incomplete')
        self.assertTrue(result['steps'][0]['error_record_seen'])

    def test_credential_script_rejected_before_launch(self):
        self.task['steps'][0]['script'] = "Write-Output 'password=unsafe'"
        with self.assertRaises(ValueError):
            ssh_task.validate_task(self.task)

    def test_credential_context_rejected(self):
        self.task['context']['environment']['token'] = 'do-not-log'
        with self.assertRaises(ValueError):
            ssh_task.validate_task(self.task)

    def test_host_option_injection_rejected(self):
        self.task['target']['ssh_target'] = '-oProxyCommand=evil'
        with self.assertRaises(ValueError):
            ssh_task.validate_task(self.task)

    def test_background_mode_rejected(self):
        self.task['execution_mode'] = 'background'
        with self.assertRaises(ValueError):
            ssh_task.validate_task(self.task)

    def test_preview_does_not_connect(self):
        path = self.root / 'task.json'; path.write_text(json.dumps(self.task))
        with patch.object(sys, 'argv', ['ssh_task.py', str(path)]), redirect_stdout(io.StringIO()), patch.object(ssh_task.subprocess, 'Popen') as launch:
            self.assertEqual(ssh_task.main(), 0)
            launch.assert_not_called()

    def test_missing_runtime_is_logged_as_failed(self):
        with patch.object(ssh_task.subprocess, 'Popen', side_effect=FileNotFoundError('ssh missing')), redirect_stdout(io.StringIO()):
            result = ssh_task.execute(self.task)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['steps'][0]['status'], 'launch_failed')

    def test_native_error_guard_and_utf8_are_in_transmitted_wrapper(self):
        _, wrapped = ssh_task.command(self.task, self.task['steps'][0], 'TEST__')
        self.assertIn("$ErrorActionPreference = 'Stop'", wrapped)
        self.assertIn('UTF8Encoding', wrapped)
        self.assertIn('function Invoke-CheckedNative', wrapped)
        self.assertIn('if ($LASTEXITCODE -ne 0)', wrapped)
        self.assertNotIn('SilentlyContinue', wrapped.replace("$ProgressPreference = 'SilentlyContinue'", ''))


if __name__ == '__main__':
    unittest.main()
