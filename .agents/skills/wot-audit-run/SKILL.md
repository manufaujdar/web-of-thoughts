---
name: wot-audit-run
description: Independently audit Web of Thoughts experiment records and claims. Use when reviewing a run, comparison, ablation, result summary, or proposed protocol change for schema compliance, budget mismatch, leakage, hidden-reasoning capture, post-hoc tuning, weak evidence, or unsupported superiority claims.
---

# Audit a Web of Thoughts run

Remain report-only and do not review your own implementation as independent evidence.

1. Read `AGENTS.md`, the frozen protocol, `docs/04-evaluation.md`,
   `schemas/run.schema.json`, run records, baseline records, and analysis artifacts.
2. Check record completeness, graph type validity, budgets, stopping behavior,
   failures, exclusions, provenance, and whether stored rationales avoid private
   hidden reasoning.
3. Compare model, prompt access, tools, retrieval, retries, latency, and accounting
   across WoT and every baseline.
4. Look for task contamination, evaluator leakage, self-grading, cherry-picked
   trials, outcome-dependent reruns, post-hoc metrics, and unreported null results.
5. Recompute or spot-check reported aggregates and confirm uncertainty and resource
   use accompany quality claims.

Return severity-ranked findings, evidence locations, invalidated claims, required
reruns, and residual uncertainty. Passing schema validation alone is not evidence
that the experiment is fair or externally valid.
