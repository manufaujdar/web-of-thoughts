#!/usr/bin/env python3
"""Offline repository gates; no application GitHub writes or provider calls."""
import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(argv):
    print("+ " + " ".join(argv), flush=True)
    return subprocess.run(argv, cwd=ROOT, check=False).returncode

def tool(name):
    candidates = [ROOT / "tools/docs/node_modules/.bin" / name, ROOT / "node_modules/.bin" / name, ROOT / "frontend/node_modules/.bin" / name,
                  Path.home() / ".local/share/manu-quality-tools/node_modules/.bin" / name]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    binary = shutil.which(name)
    if not binary:
        raise RuntimeError(f"Missing {name}; install the pinned tools documented in TOOLING.md")
    return binary

def docs(base=None):
    paths = ["TOOLING.md"]
    if base:
        if not re.fullmatch(r"[0-9a-f]{40,64}", base):
            raise ValueError("Expected a full Git base SHA")
        changed = subprocess.check_output(["git", "diff", "--name-only", "--diff-filter=ACMRT", "-z", base, "HEAD"], cwd=ROOT).decode().split("\0")
        paths += [p for p in changed if p.endswith(".md") and (p.startswith("docs/") or p in ("README.md", "CONTRIBUTING.md", "AGENTS.md"))]
    paths = sorted({p for p in paths if (ROOT / p).is_file()})
    for argv in ([tool("markdownlint"), "--config", ".markdownlint.json", *paths],
                 [tool("lychee"), "--offline", "--include-fragments", "--root-dir", str(ROOT), *paths]):
        result = run(argv)
        if result:
            return result
    workflows = sorted(str(p.relative_to(ROOT)) for p in (ROOT / ".github/workflows").glob("*.yml"))
    if workflows:
        for argv in ([tool("actionlint"), *workflows], [tool("zizmor"), "--no-progress", "--offline", "--min-severity", "medium", *workflows]):
            result = run(argv)
            if result:
                return result
    return run([sys.executable, "-m", "unittest", "discover", "-s", "tools", "-p", "test_tooling*.py", "-v"])

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs", action="store_true", help="Scoped engineering Markdown and workflow checks only")
    parser.add_argument("--application", action="store_true", help="Application checks only, used by CI")
    parser.add_argument("--tooling", action="store_true", help="Docs, workflow, tool contracts and offline secrets only")
    parser.add_argument("--advisory", action="store_true", help="Report Knip findings without deleting files or blocking")
    parser.add_argument("--base", default=os.environ.get("MANU_QUALITY_BASE"), help="Before-push commit SHA")
    args = parser.parse_args()
    try:
        if args.advisory:
            result = run(["npm", "--prefix", "frontend", "run", "check:unused"])
            return result
        if not args.application:
            result = docs(args.base)
            if result or args.docs:
                return result
            log_opts = f"{args.base}..HEAD" if args.base else "-1"
            result = run([tool("betterleaks"), "git", "--redact", "--log-opts", log_opts])
            if result:
                return result
            if args.tooling:
                return 0
        python = str(ROOT / '.venv/bin/python') if (ROOT / '.venv/bin/python').is_file() else sys.executable
        for argv in ([python, "tools/validate_repository.py"], [python, "-m", "unittest", "discover", "-s", "tests", "-v"],
                     [python, "-m", "compileall", "-q", "wot_app", "tools", "tests"],
                     ["npm", "--prefix", "frontend", "test"], ["npm", "--prefix", "frontend", "run", "build"], ["npm", "--prefix", "frontend", "run", "test:browser"]):
            result = run(argv)
            if result:
                return result
        return 0
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Quality gate failed: {error}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
