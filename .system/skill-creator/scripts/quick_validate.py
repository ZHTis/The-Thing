#!/usr/bin/env python3
"""Official Agent Skills schema validation plus unfinished-scaffold checks.

Install the repository's requirements-validation.txt into the validation
virtual environment. Schema rules come from skills-ref, not a second allowlist.
"""
import re
import sys
from pathlib import Path


def validate_skill(skill_path):
    skill_path = Path(skill_path)
    try:
        from skills_ref import validate, read_properties
    except ImportError:
        return False, "Install requirements-validation.txt in the validation environment; skills-ref is required"
    errors = validate(skill_path)
    if errors:
        return False, "; ".join(errors)
    if read_properties(skill_path).description.lstrip().startswith("[TODO:"):
        return False, "Description contains an unfinished TODO placeholder"
    content = (skill_path / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"
    body = content[match.end() :]
    fence_marker = None
    fence_length = 0
    for line in body.splitlines():
        fence = re.match(r"^[ \t]*(?:(?:[-+*]|\d+[.)])[ \t]+)?(`{3,}|~{3,})(.*)$", line)
        if fence:
            marker = fence.group(1)
            if fence_marker is None:
                fence_marker = marker[0]
                fence_length = len(marker)
            elif (
                marker[0] == fence_marker
                and len(marker) >= fence_length
                and not fence.group(2).strip()
            ):
                fence_marker = None
                fence_length = 0
            continue

        if fence_marker is None and re.fullmatch(
            r"[ ]{0,3}\[TODO:[^\n]*\][ \t]*", line
        ):
            return False, "Skill instructions contain an unfinished TODO placeholder"

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
