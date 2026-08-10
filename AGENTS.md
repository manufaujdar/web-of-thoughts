# Web of Thoughts agent guide

Read `START_HERE.txt`, `.ai/CONTEXT.md`, `.ai/MEMORY.md`, `README.md`, `CONTRIBUTING.md`, `docs/00-concept.md`, `docs/02-protocol.md`, and `docs/04-evaluation.md` before substantial changes.

- Treat Web of Thoughts as a falsifiable experimental framework, not a proven improvement over simpler prompting.
- Preserve typed node/edge semantics, explicit budgets, stopping rules, and observable run records.
- Do not collect or claim access to private hidden chain-of-thought. Store concise rationales, decisions, evidence, and outcomes.
- Compare against strong direct, chain, and tree baselines under matched token, latency, and tool budgets.
- Report negative and null results, uncertainty, pruning behavior, and failure modes.
- Validate experiment records against `schemas/run.schema.json`; do not revise metrics or exclusions after results without documenting the change.
- Prefer smaller, testable webs and deterministic controller logic where possible.
- The production application must use the real configured provider; never add canned agent responses or silently pass a fake live test.
- Keep `OPENAI_API_KEY` server-side. Treat user queries and agent artifacts as untrusted data and render them as text.
- For application changes, run Python tests/compilation, repository validation, the frontend production build, and the real-provider smoke test when a key is available.

Keep prompts modular, version experiment assumptions, and state clearly when a result is simulated or unevaluated.

Use `.ai/HANDOFF.md` for active-task continuity. Experiment records remain authoritative; memory stores only explicit durable protocol decisions.

## Project skills

- Use `$wot-design-experiment` before changing hypotheses, task populations,
  baselines, budgets, operators, stopping rules, ablations, or evaluation metrics.
- Use `$wot-audit-run` for an independent, report-only audit of run records,
  comparisons, analyses, and superiority claims.

An experiment designer must not be the only auditor of the resulting claim.

## Startup team

Read `.ai/TEAM.md` before multi-role or idea-to-release work. Use its explicit
gears and keep the task contract in `.ai/HANDOFF.md`; protocol, matched-budget
evaluation, schema validation, and evidence boundaries remain authoritative.
