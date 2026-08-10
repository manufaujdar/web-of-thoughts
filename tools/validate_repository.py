#!/usr/bin/env python3
"""Validate repository structure and Web of Thoughts run records.

These checks establish structural admissibility, not scientific validity.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote


REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "NOTICE",
    "CITATION.cff",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "GOVERNANCE.md",
    "docs/06-research-boundaries.md",
    "docs/07-provenance.md",
    "docs/08-validation-protocol.md",
    "docs/09-application.md",
    "schemas/run.schema.json",
    "wot_app/main.py",
    "wot_app/orchestrator.py",
    "frontend/package-lock.json",
)

SENSITIVE_NAMES = {
    ".env",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
    "service-account.json",
}
SENSITIVE_SUFFIXES = {".pem", ".p12", ".pfx", ".key"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[oprsu]_[A-Za-z0-9]{30,}\b"),
)
IGNORED_PARTS = {".git", ".venv", "node_modules", "dist", "build", "__pycache__", "data", "artifacts"}


@dataclass(frozen=True)
class Finding:
    path: str
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.message}"


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema_document(schema: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(schema, dict):
        return ["schema root must be an object"]
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema must declare JSON Schema draft 2020-12")
    required = schema.get("required", [])
    for field in ("spec_version", "run_id", "task_id", "method", "model", "budget", "result"):
        if field not in required:
            errors.append(f"schema does not require {field!r}")

    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return errors

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes version-specific exception classes
        errors.append(f"invalid JSON Schema: {exc}")
    return errors


def basic_run_errors(run: Any) -> list[str]:
    """Provide dependency-free safety checks for a run record."""
    if not isinstance(run, dict):
        return ["run root must be an object"]

    errors: list[str] = []
    for field in ("spec_version", "run_id", "task_id", "method", "model", "budget", "result"):
        if field not in run:
            errors.append(f"missing required field {field!r}")

    if errors:
        return errors

    if run["method"] not in {"direct", "cot", "self_consistency", "tot", "got", "wot"}:
        errors.append("method is not in the controlled vocabulary")

    model = run["model"]
    if not isinstance(model, dict) or not all(model.get(key) for key in ("provider", "name")):
        errors.append("model must identify non-empty provider and name")

    budget = run["budget"]
    if not isinstance(budget, dict):
        errors.append("budget must be an object")
    else:
        if type(budget.get("max_calls")) is not int or budget.get("max_calls", 0) < 1:
            errors.append("budget.max_calls must be a positive integer")
        if type(budget.get("max_total_tokens")) is not int or budget.get("max_total_tokens", 0) < 1:
            errors.append("budget.max_total_tokens must be a positive integer")

    result = run["result"]
    if not isinstance(result, dict):
        errors.append("result must be an object")
    else:
        if result.get("status") not in {"success", "failure", "invalid", "partial"}:
            errors.append("result.status is invalid")
        if result.get("termination_reason") not in {
            "bypassed", "converged", "verified_threshold", "dominated_alternatives",
            "low_marginal_value", "budget_exhausted", "error",
        }:
            errors.append("result.termination_reason is invalid")

    usage = run.get("usage")
    if isinstance(usage, dict) and isinstance(budget, dict):
        calls = usage.get("calls")
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        max_calls = budget.get("max_calls")
        max_tokens = budget.get("max_total_tokens")

        for field, value in (
            ("calls", calls),
            ("input_tokens", input_tokens),
            ("output_tokens", output_tokens),
        ):
            if value is not None and (type(value) is not int or value < 0):
                errors.append(f"usage.{field} must be a non-negative integer")

        total_tokens = (
            input_tokens + output_tokens
            if type(input_tokens) is int and type(output_tokens) is int
            else None
        )
        exceeded = (
            type(calls) is int
            and type(max_calls) is int
            and calls > max_calls
        ) or (
            type(total_tokens) is int
            and type(max_tokens) is int
            and total_tokens > max_tokens
        )
        if exceeded and result.get("status") != "invalid":
            errors.append("actual usage exceeds budget but result is not marked invalid")

    return errors


def full_run_errors(run: Any, schema: dict[str, Any]) -> list[str]:
    errors = basic_run_errors(run)
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return errors

    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(run), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        message = f"{location}: {error.message}"
        if message not in errors:
            errors.append(message)
    return errors


def iter_repository_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS or part.endswith(".egg-info") for part in path.parts):
            continue
        yield path


def check_markdown_links(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_repository_files(root):
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            clean_target = unquote(target.split("#", 1)[0])
            resolved = (path.parent / clean_target).resolve()
            if not resolved.exists():
                findings.append(Finding(str(path.relative_to(root)), f"broken local link: {target}"))
    return findings


def check_sensitive_paths(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_repository_files(root):
        if path.name in SENSITIVE_NAMES or path.suffix.lower() in SENSITIVE_SUFFIXES:
            findings.append(Finding(str(path.relative_to(root)), "likely sensitive artifact must not be committed"))
    return findings


def check_secret_patterns(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_repository_files(root):
        if path.suffix.lower() not in {".py", ".md", ".json", ".yml", ".yaml", ".toml", ".txt", ".ts", ".tsx", ".js"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            findings.append(Finding(str(path.relative_to(root)), "possible committed credential pattern"))
    return findings


def validate_repository(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            findings.append(Finding(relative, "required repository file is missing"))

    schema_path = root / "schemas/run.schema.json"
    if not schema_path.is_file():
        return findings

    try:
        schema = load_json(schema_path)
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(Finding("schemas/run.schema.json", f"cannot parse schema: {exc}"))
        return findings

    for message in validate_schema_document(schema):
        findings.append(Finding("schemas/run.schema.json", message))

    for path in sorted((root / "experiments").glob("**/runs/*.json")):
        try:
            run = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(Finding(str(path.relative_to(root)), f"cannot parse run: {exc}"))
            continue
        for message in full_run_errors(run, schema):
            findings.append(Finding(str(path.relative_to(root)), message))

    findings.extend(check_markdown_links(root))
    findings.extend(check_sensitive_paths(root))
    findings.extend(check_secret_patterns(root))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    root = args.root.resolve()
    findings = validate_repository(root)
    if findings:
        print(f"Validation failed with {len(findings)} finding(s):", file=sys.stderr)
        for finding in findings:
            print(f"- {finding.render()}", file=sys.stderr)
        return 1
    print("Repository validation passed (structural checks only; no scientific claim implied).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
