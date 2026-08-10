# Web of Thoughts

Web of Thoughts (WoT) is an experimental prompting and inference framework for solving complex problems through a **typed, multidimensional network of candidate thoughts**. It extends linear chains and branching trees with explicit relations among ideas: support, contradiction, dependency, refinement, analogy, evidence, and synthesis.

This repository is a research foundation, not a claim of proven superiority. Its purpose is to turn the idea into a precise, testable method whose accuracy, cost, latency, robustness, and failure modes can be compared with simpler baselines.

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
- [`docs/glossary.md`](docs/glossary.md) — stable terminology
- [`prompts/`](prompts) — modular prompt templates
- [`schemas/run.schema.json`](schemas/run.schema.json) — experiment record contract
- [`experiments/README.md`](experiments/README.md) — experiment naming and reporting conventions
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — standards for changing the technique

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

## Current status

**Phase 0 — specification.** The framework below is a falsifiable proposal. Names, operators, scoring formulas, and default thresholds are versioned hypotheses until experiments support them.

## Research principles

- Prefer a smaller useful web over maximal branching.
- Separate generation from evaluation when possible.
- Track uncertainty and evidence provenance explicitly.
- Use external verification for externally checkable claims.
- Never treat model self-confidence as calibrated probability by default.
- Compare against strong, budget-matched baselines.
- Preserve final rationale and evidence, not private hidden reasoning traces.
- Report negative and null results.

