# Web of Thoughts

Complex problems often need more than one candidate answer, but a larger prompt or a hidden reasoning trace does not make the process inspectable. Web of Thoughts (WoT) is an experimental framework for representing candidate ideas as a typed, multidimensional network with explicit relations such as support, contradiction, dependency, refinement, analogy, evidence, and synthesis. The included application turns that model into a bounded research workbench with multi-agent exploration, peer review, and evaluation records.

This repository is a local-first research foundation, not a claim of proven superiority or a production-ready autonomous system. Its purpose is to turn the idea into a precise, testable method whose accuracy, cost, latency, robustness, and failure modes can be compared with simpler baselines.

> **Evidence status:** functional research prototype, unvalidated method. No completed evaluation in this repository establishes that WoT outperforms direct prompting, Chain of Thought, Tree of Thoughts, or Graph of Thoughts.

## Live application

The included application runs six role-specific OpenAI agents, streams their work in real time, connects their public decision artifacts through typed graph edges, performs cross-agent peer review, and asks a master evaluator to compare all viable possibilities before answering. Production code has no canned-response fallback: a run requires a server-side `OPENAI_API_KEY` and uses the OpenAI Responses API.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cd frontend && npm install && npm run build && cd ..

export OPENAI_API_KEY='your-key' # keep this local
wot-server
```

Open `http://127.0.0.1:8000`. See the [application guide](docs/09-application.md) for Docker, API, persistence, privacy, and live-smoke details.

## Core hypothesis

For problems that benefit from decomposition, alternative perspectives, verification, and recombination, an LLM can reason more reliably and efficiently when it:

1. maps the problem across a small set of relevant dimensions;
2. generates diverse candidate thoughts rather than one long chain;
3. creates typed links between related candidates;
4. challenges and verifies high-impact claims;
5. synthesizes compatible partial solutions;
6. prunes redundant or weak regions under a fixed budget; and
7. stops when additional exploration has low expected value.

The word **web** refers to this controlled network. It does not mean exhaustive enumeration, hidden chain-of-thought collection, or an arbitrarily dense graph.

## Repository map

- [`docs/00-concept.md`](docs/00-concept.md) — definition, scope, novelty, and design principles
- [`docs/01-formal-model.md`](docs/01-formal-model.md) — graph objects, operators, scores, budgets, and stopping rules
- [`docs/02-protocol.md`](docs/02-protocol.md) — end-to-end WoT procedure
- [`docs/03-research-landscape.md`](docs/03-research-landscape.md) — intellectual context and differentiation
- [`docs/04-evaluation.md`](docs/04-evaluation.md) — benchmarks, baselines, metrics, ablations, and validity rules
- [`docs/05-roadmap.md`](docs/05-roadmap.md) — staged research plan
- [`docs/06-research-boundaries.md`](docs/06-research-boundaries.md) — supported use, safety, privacy, and deployment limits
- [`docs/07-provenance.md`](docs/07-provenance.md) — model, prompt, task, and evidence provenance
- [`docs/08-validation-protocol.md`](docs/08-validation-protocol.md) — deterministic quality gates and release checks
- [`docs/09-application.md`](docs/09-application.md) — live application architecture, setup, API, persistence, and deployment boundary
- [`docs/glossary.md`](docs/glossary.md) — stable terminology
- [`prompts/`](prompts) — modular prompt templates
- [`schemas/run.schema.json`](schemas/run.schema.json) — experiment record contract
- [`experiments/README.md`](experiments/README.md) — experiment naming and reporting conventions
- [`templates/`](templates) — model-card and dataset-card templates
- [`wot_app/`](wot_app) — FastAPI, OpenAI, orchestration, streaming, and SQLite backend
- [`frontend/`](frontend) — responsive React/TypeScript research workbench
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — standards for changing the technique
- [`GOVERNANCE.md`](GOVERNANCE.md) and [`SECURITY.md`](SECURITY.md) — decision and security processes

## Minimal WoT loop

```text
frame -> seed -> expand -> connect -> challenge -> synthesize -> select -> stop
```

At every iteration, the controller asks: **Which next operation has the highest expected information or solution value per unit of budget?**

## Quick start

1. Select a task with a checkable outcome.
2. Run direct prompting, Chain of Thought, and Tree of Thoughts baselines under recorded budgets.
3. Fill in [`prompts/00-controller.md`](prompts/00-controller.md) and execute a WoT run.
4. Save the result using [`experiments/run-template.md`](experiments/run-template.md) and validate metadata against the JSON schema.
5. Compare task quality and total resource use; do not report quality without cost and latency.

## Validate the repository

The repository includes deterministic structural checks and synthetic tests:

```bash
python3 tools/validate_repository.py
python3 -m unittest discover -s tests -v
python3 -m compileall -q wot_app tools tests
npm ci --prefix frontend
npm run build --prefix frontend
git diff --check
```

Install `.[dev]` to enable complete JSON Schema validation through `jsonschema`. Passing these checks means the repository and run records are structurally admissible; it is not evidence that an experiment is fair or that WoT is effective.

## Current status

**Prototype implementation; Phase-0 evidence.** The system is executable, but the method remains a falsifiable proposal. Names, operators, scoring formulas, role topology, and defaults are versioned hypotheses until controlled experiments support them. A working interface is not evidence of superior reasoning.

## Research principles

- Prefer a smaller useful web over maximal branching.
- Separate generation from evaluation when possible.
- Track uncertainty and evidence provenance explicitly.
- Use external verification for externally checkable claims.
- Never treat model self-confidence as calibrated probability by default.
- Compare against strong, budget-matched baselines.
- Preserve final rationale and evidence, not private hidden reasoning traces.
- Report negative and null results.

## Responsible research

Use synthetic or explicitly redistributable fixtures by default. Do not commit credentials, private conversations, personal or regulated data, proprietary prompts, restricted benchmarks, raw provider logs, unverified model weights, or private hidden reasoning. Treat model and tool output as untrusted and externally verify consequential claims.

See the [research boundaries](docs/06-research-boundaries.md), [provenance policy](docs/07-provenance.md), and [security policy](SECURITY.md) before integrating external models, datasets, evaluators, or tools.

## License and citation

Web of Thoughts is licensed under the [Apache License 2.0](LICENSE). Use [`CITATION.cff`](CITATION.cff) and cite the exact version or commit used; repository structure and citation do not imply scientific validation.
