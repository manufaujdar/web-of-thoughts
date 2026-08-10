---
name: wot-design-experiment
description: Design falsifiable, budget-matched experiments for the Web of Thoughts framework. Use when selecting tasks, baselines, operators, graph types, stopping rules, ablations, metrics, run records, or preregistered hypotheses before evaluating WoT.
---

# Design a Web of Thoughts experiment

Read `AGENTS.md`, `docs/02-protocol.md`, `docs/04-evaluation.md`, the run schema,
and the smallest relevant prior experiment.

1. State a directional hypothesis, checkable task population, expected mechanism,
   primary outcome, and a result that would count against WoT.
2. Choose strong direct, chain, and tree baselines. Match token, latency, tool,
   retrieval, retry, and model budgets or disclose each unavoidable mismatch.
3. Freeze node and edge types, controller operations, pruning, stopping rules,
   evaluator, trial count, seeds where applicable, exclusions, and analysis before
   inspecting results.
4. Include ablations that isolate expansion, cross-links, challenge, synthesis,
   pruning, and adaptive stopping only when those mechanisms are present.
5. Record quality, cost, latency, failures, graph size, pruning behavior, and
   uncertainty. Preserve concise rationale and evidence, never hidden chain-of-thought.
6. Create schema-valid run records and keep simulated or pilot evidence clearly
   separate from confirmatory results.

Handoff the preregistered protocol, fairness table, planned records, validity
threats, files changed, and validation method. Do not claim superiority from an
unmatched, post-hoc, or single-task comparison.
