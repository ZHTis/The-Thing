import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("quick_validate_standard", ROOT / ".system/skill-creator/scripts/quick_validate.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class QuickValidatorStandardTests(unittest.TestCase):
    def check(self, front, body="# Example\n"):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "example"
            folder.mkdir()
            (folder / "SKILL.md").write_text("---\n" + front + "\n---\n" + body)
            return MODULE.validate_skill(folder)

    def test_standard_compatibility_is_accepted(self):
        self.assertTrue(self.check("name: example\ndescription: A useful skill.\ncompatibility: Python 3 and Windows PowerShell")[0])

    def test_unknown_top_level_field_is_rejected(self):
        self.assertFalse(self.check("name: example\ndescription: A useful skill.\nnot-a-standard-field: true")[0])

    def test_invalid_compatibility_type_is_rejected(self):
        # The official parser treats scalars as strings; a sequence is invalid.
        self.assertFalse(self.check("name: example\ndescription: A useful skill.\ncompatibility:\n  - Python")[0])

    def test_missing_required_description_is_rejected(self):
        self.assertFalse(self.check("name: example")[0])

    def test_unfinished_description_is_rejected(self):
        self.assertFalse(self.check('name: example\ndescription: "[TODO: write actual description]"')[0])

    def test_unfinished_scaffold_is_rejected(self):
        self.assertFalse(self.check("name: example\ndescription: A useful skill.", "[TODO: write actual steps]\n")[0])

    def test_todo_inside_example_code_is_not_scaffold(self):
        self.assertTrue(self.check("name: example\ndescription: A useful skill.", "```text\n[TODO: example input]\n```\n")[0])


if __name__ == "__main__":
    unittest.main()
