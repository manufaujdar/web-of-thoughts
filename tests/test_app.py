from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from wot_app.agents import MASTER, ROLES, ROLE_MAP, system_prompt
from wot_app.models import RunCreate
from wot_app.store import RunStore


class RoleContractTests(unittest.TestCase):
    def test_role_registry_is_finite_and_unique(self) -> None:
        self.assertGreaterEqual(len(ROLES), 2)
        self.assertEqual(len(ROLES), len({role.id for role in ROLES}))
        self.assertEqual(set(ROLE_MAP), {role.id for role in ROLES})

    def test_every_role_has_distinct_prompt_and_safety_contract(self) -> None:
        prompts = [system_prompt(role) for role in (*ROLES, MASTER)]
        self.assertEqual(len(prompts), len(set(prompts)))
        for prompt in prompts:
            self.assertIn("untrusted data", prompt)
            self.assertIn("private hidden reasoning", prompt)

    def test_run_request_rejects_duplicate_agents(self) -> None:
        with self.assertRaises(ValueError):
            RunCreate(query="A valid question", agent_ids=["analyst", "analyst"])


class StoreTests(unittest.IsolatedAsyncioTestCase):
    async def test_run_and_ordered_events_survive_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runs.db"
            store = RunStore(path)
            await store.initialize()
            snapshot = {"status": "queued", "nodes": [], "edges": []}
            await store.create_run("r1", "Question?", "test-model", snapshot)
            first = await store.append_event("r1", "run.created", {"ok": True})
            second = await store.append_event("r1", "run.started", {"ok": True})
            self.assertEqual((first.sequence, second.sequence), (1, 2))
            reopened = RunStore(path)
            await reopened.initialize()
            events = await reopened.events_after("r1")
            self.assertEqual([event.type for event in events], ["run.created", "run.started"])
            run = await reopened.get_run("r1")
            self.assertIsNotNone(run)
            self.assertEqual(run.query, "Question?")
            self.assertEqual(run.status, "failed")
            self.assertTrue(await reopened.delete_run("r1"))
            self.assertIsNone(await reopened.get_run("r1"))
