import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from ssh_task import AuditLog, LOG_MAX_BYTES, LOG_TOTAL_FILES


class RotationTests(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual((LOG_MAX_BYTES, LOG_TOTAL_FILES), (20_000_000, 10))

    def test_utf8_bound_order_and_retention(self):
        with tempfile.TemporaryDirectory() as root:
            p = Path(root) / 'audit.jsonl'
            rows = [json.dumps({'n': n, 'text': '中文'}, ensure_ascii=False)+'\n' for n in range(13)]
            with AuditLog(p, max_bytes=40) as out:
                for row in rows:
                    out.write(row)
            files = [p] + [p.with_name(p.name+'.'+str(n)) for n in range(1, 10)]
            self.assertTrue(all(f.stat().st_size <= 40 for f in files))
            self.assertEqual([json.loads(f.read_text())['n'] for f in files], list(range(12, 2, -1)))
            self.assertFalse(p.with_name(p.name+'.10').exists())

    def test_exact_boundary_and_resume(self):
        with tempfile.TemporaryDirectory() as root:
            p = Path(root) / 'audit.jsonl'
            with AuditLog(p, max_bytes=4) as out:
                out.write('a\n'); out.write('b\n')
            self.assertFalse(p.with_name(p.name+'.1').exists())
            with AuditLog(p, max_bytes=4) as out:
                out.write('c\n')
            self.assertEqual(p.read_text(), 'c\n')
            self.assertEqual(p.with_name(p.name+'.1').read_text(), 'a\nb\n')

    def test_oversized_event_preserves_existing(self):
        with tempfile.TemporaryDirectory() as root:
            p = Path(root) / 'audit.jsonl'
            p.write_text('old\n')
            with AuditLog(p, max_bytes=5) as out:
                with self.assertRaises(ValueError):
                    out.write('中文\n')
            self.assertEqual(p.read_text(), 'old\n')

    def test_competing_writer_rejected_then_lock_released(self):
        with tempfile.TemporaryDirectory() as root:
            p = Path(root) / 'audit.jsonl'
            with AuditLog(p):
                with self.assertRaises(OSError):
                    with AuditLog(p):
                        self.fail('second writer acquired lock')
            with AuditLog(p) as out:
                out.write('{}\n')


if __name__ == '__main__':
    unittest.main()
