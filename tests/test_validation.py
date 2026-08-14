from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.validate_repository import (
    basic_run_errors,
    check_markdown_links,
    load_json,
    validate_repository,
    validate_schema_document,
)


ROOT = Path(__file__).resolve().parents[1]


class RunValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(ROOT / "schemas/run.schema.json")
        cls.valid_run = load_json(ROOT / "tests/fixtures/valid-run.json")

    def test_schema_is_well_formed(self) -> None:
        self.assertEqual(validate_schema_document(self.schema), [])

    def test_fixture_passes_dependency_free_checks(self) -> None:
        self.assertEqual(basic_run_errors(self.valid_run), [])

    def test_missing_required_field_fails(self) -> None:
        run = copy.deepcopy(self.valid_run)
        del run["task_id"]
        self.assertIn("missing required field 'task_id'", basic_run_errors(run))

    def test_budget_overrun_requires_invalid_status(self) -> None:
        run = copy.deepcopy(self.valid_run)
        run["usage"]["output_tokens"] = 1000
        self.assertTrue(any("exceeds budget" in item for item in basic_run_errors(run)))
        run["result"]["status"] = "invalid"
        self.assertFalse(any("exceeds budget" in item for item in basic_run_errors(run)))

    def test_malformed_usage_fails_without_crashing(self) -> None:
        run = copy.deepcopy(self.valid_run)
        run["usage"]["input_tokens"] = "unknown"
        errors = basic_run_errors(run)
        self.assertIn("usage.input_tokens must be a non-negative integer", errors)

    def test_repository_passes_all_quality_gates(self) -> None:
        self.assertEqual(validate_repository(ROOT), [])

    def test_all_markdown_is_utf8_and_links_resolve(self) -> None:
        for path in ROOT.rglob("*.md"):
            if ".git" not in path.parts:
                path.read_text(encoding="utf-8")
        self.assertEqual(check_markdown_links(ROOT), [])

    def test_fixture_is_explicitly_synthetic(self) -> None:
        notes = self.valid_run["result"]["notes"].lower()
        self.assertIn("synthetic", notes)
        self.assertIn("not experimental evidence", notes)


if __name__ == "__main__":
    unittest.main()
