#!/usr/bin/env python3
"""Validate the GitHub Actions workflow files before pushing.

A YAML mistake in a workflow only shows up after a push, as a failed run with
"Invalid workflow file" — this catches it locally in a second. The classic one:
an unquoted value containing ": ", which YAML reads as a nested key.

    python3 tools/check_workflows.py
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"


def main():
    try:
        import yaml
    except ImportError:
        print("PyYAML is not installed — skipping (pip install pyyaml)")
        return 0

    files = sorted(WORKFLOWS.glob("*.yml")) + sorted(WORKFLOWS.glob("*.yaml"))
    if not files:
        print("no workflow files found")
        return 0

    bad = 0
    for f in files:
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            print(f"{f.name}: INVALID — {e}")
            bad += 1
            continue
        jobs = list((data or {}).get("jobs", {}))
        if not jobs:
            print(f"{f.name}: parses, but declares no jobs")
            bad += 1
        else:
            print(f"{f.name}: ok — jobs: {', '.join(jobs)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
