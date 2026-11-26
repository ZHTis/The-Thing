"""Protect the official layout from the archived Codex-only neutral-slot variant."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image, ImageDraw
from plugin_location import plugin_skill_dir


class OfficialSheetContractTests(unittest.TestCase):
    def validate_fixture(self, extra_neutral):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'fixture.png'
            image = Image.new('RGBA', (1536, 2288), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            counts = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
            for row, count in enumerate(counts):
                for column in range(count):
                    left, top = column * 192 + 60, row * 208 + 50
                    draw.rectangle((left, top, left + 63, top + 95), fill=(30, 90, 140, 255))
            if extra_neutral:
                draw.rectangle((6 * 192 + 60, 50, 6 * 192 + 123, 145), fill=(30, 90, 140, 255))
            image.save(path)
            process = subprocess.run([sys.executable, str(plugin_skill_dir() / 'scripts/validate_atlas.py'), str(path), '--require-v2'], capture_output=True, text=True)
            return process.returncode, json.loads(process.stdout)

    def test_official_v2_keeps_only_73_required_cells(self):
        code, report = self.validate_fixture(False)
        self.assertEqual(code, 0, report['errors'])
        self.assertTrue(report['ok'])

    def test_archived_extra_neutral_cell_is_rejected(self):
        code, report = self.validate_fixture(True)
        self.assertNotEqual(code, 0)
        self.assertTrue(any('unused column 6 is not transparent' in error for error in report['errors']))


if __name__ == '__main__':
    unittest.main()
