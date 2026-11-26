#!/usr/bin/env python3
"""Run preserved Apache-licensed regression fixtures against installed work-pets.

Python 3.10+ with Pillow. No image generation, user pet files, network, Library
or Pets API mutation. The official plugin remains external to this package.
"""
import argparse
import importlib.util
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=['work', 'codex'], default='work', help='Choose the official Work contract or archived Codex compatibility tests')
    parser.add_argument('--plugin-skill-dir', type=Path, help='Active official work-pets skills/create-pet directory')
    args = parser.parse_args()
    if importlib.util.find_spec("PIL") is None:
        print("Pillow is unavailable in this Python environment; checks were not run.", file=sys.stderr)
        return 2
    environment = os.environ.copy()
    if args.plugin_skill_dir:
        environment['WORK_PETS_CREATE_SKILL_DIR'] = str(args.plugin_skill_dir.expanduser().resolve())
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    skill_root = Path(__file__).resolve().parents[1]
    tests = skill_root / 'tests' if args.target == 'work' else skill_root / 'compat/codex/tests'
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(tests), '-v'], env=environment)
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
