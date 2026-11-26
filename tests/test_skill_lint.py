import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lint_skills import lint


class SkillLintTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "example"
        self.skill.mkdir()
        self.entry = self.skill / "SKILL.md"
        self.entry.write_text("---\nname: example\ndescription: Test a concrete fixture when testing lint.\nmetadata:\n  the-thing.category: test\n---\n# Example\n")
        (self.root / "taxonomy.json").write_text(json.dumps({"test": {"label": "Test", "skills": ["example"]}}))
        (self.root / "FUNCTIONAL-INDEX.md").write_text("[example](example/SKILL.md)\n")

    def codes(self):
        return {item["rule"] for item in lint(self.root)["diagnostics"]}

    def test_valid_skill(self):
        self.assertEqual(self.codes(), set())

    def test_broken_resource(self):
        self.entry.write_text(self.entry.read_text() + "[guide](references/missing.md)\n")
        self.assertIn("LINK001", self.codes())

    def test_non_string_metadata(self):
        self.entry.write_text(self.entry.read_text().replace("  the-thing.category: test", "  the-thing.category: test\n  version: 12"))
        self.assertIn("META001", self.codes())

    def test_invalid_yaml_is_reported(self):
        self.entry.write_text("---\nname: [unterminated\n---\n")
        self.assertIn("SPEC001", self.codes())

    def test_duplicate_yaml_key(self):
        self.entry.write_text(self.entry.read_text().replace("name: example", "name: example\nname: example"))
        self.assertIn("YAML001", self.codes())

    def test_duplicate_taxonomy_members(self):
        (self.root / "taxonomy.json").write_text(json.dumps({"test": {"skills": ["example", "example"]}}))
        self.assertIn("CAT001", self.codes())

    def test_invalid_python_is_not_executed(self):
        (self.skill / "bad.py").write_text("def broken(:\n")
        self.assertIn("PY001", self.codes())

    def test_explicit_policy_is_required(self):
        self.entry.write_text(self.entry.read_text().replace("  the-thing.category: test", "  the-thing.category: test\n  the-thing.invocation: explicit"))
        self.assertIn("HOST001", self.codes())

    def test_code_examples_are_not_resource_dependencies(self):
        self.entry.write_text(self.entry.read_text() + "```markdown\n[example](not-installed.md)\n```\n")
        self.assertNotIn("LINK001", self.codes())

    def test_index_coverage(self):
        (self.root / "FUNCTIONAL-INDEX.md").write_text("")
        self.assertIn("INDEX001", self.codes())


if __name__ == "__main__":
    unittest.main()
