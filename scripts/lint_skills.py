#!/usr/bin/env python3
"""Lint all skills and bundled Python/YAML without executing skill workflows."""
import argparse
import ast
import json
import re
from pathlib import Path
import yaml
from validate_skills import check


class UniqueKeysLoader(yaml.SafeLoader):
    """Reject duplicate keys which ordinary YAML loaders silently overwrite."""


def unique_mapping(loader, node):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in mapping:
            raise ValueError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node)
    return mapping


UniqueKeysLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def lint(root):
    diagnostics = []
    def add(code, path, message, line=1):
        diagnostics.append({"rule": code, "path": path, "line": line, "message": message})
    try:
        results = check(root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        add("CAT001", "taxonomy.json", str(exc))
        results = []
    for result in results:
        for message in result["errors"]:
            code = re.match(r"\[([A-Z]+[0-9]+)\]", message)
            add(code.group(1) if code else "SPEC001", result["path"] + "/SKILL.md", message)
    index = (root / "FUNCTIONAL-INDEX.md").read_text() if (root / "FUNCTIONAL-INDEX.md").exists() else ""
    for result in results:
        if f'({result["path"]}/SKILL.md)' not in index:
            add("INDEX001", "FUNCTIONAL-INDEX.md", "Add the index link for " + result["path"])
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in {".git", ".venv", "__pycache__"} for part in path.relative_to(root).parts):
            continue
        rel = str(path.relative_to(root))
        try:
            if path.suffix == ".py":
                ast.parse(path.read_text(), filename=rel)
            elif path.suffix in {".yaml", ".yml"}:
                yaml.load(path.read_text(), Loader=UniqueKeysLoader)
            elif path.name == "SKILL.md":
                raw = path.read_text()
                if raw.startswith("---"):
                    yaml.load(raw.split("---", 2)[1], Loader=UniqueKeysLoader)
        except SyntaxError as exc:
            add("PY001", rel, "Fix Python syntax: " + str(exc.msg), exc.lineno or 1)
        except (yaml.YAMLError, ValueError, IndexError, UnicodeError) as exc:
            add("YAML001", rel, "Fix YAML syntax or duplicate keys: " + str(exc))
    return {"checked": len(results), "errors": len(diagnostics), "diagnostics": diagnostics}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = lint(args.root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result["diagnostics"]:
            print(f'{item["path"]}:{item["line"]}: error {item["rule"]}: {item["message"]}')
        print(f'Lint: {result["checked"]} skills, {result["errors"]} errors.')
    raise SystemExit(1 if result["errors"] else 0)


if __name__ == "__main__":
    main()
