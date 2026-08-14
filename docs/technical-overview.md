# Technical overview

Status: Phase 0 specification.

## Repository contracts

- Markdown documents define the hypothesis, formal model, protocol, research landscape, evaluation, roadmap, and glossary.
- Prompt files define modular controller and role prompts.
- JSON Schema defines required run metadata, model, budget, configuration, usage, and result fields.
- experiments/ contains the run template and reporting conventions.
- No runtime dependencies, package manifest, service entrypoint, or executable test suite is currently present.

## Required implementation baseline

When a runner is added, keep controller logic deterministic where possible,
version prompt/schema/protocol inputs, validate every record, and separate
generation from evaluation. Provide a CLI or library entrypoint, reproducible
offline fixtures, schema tests, budget accounting, failure/timeout handling,
and artifact redaction.

## Research validation

A result is not decision-ready until task population, outcome rubric, baseline,
budget, model/version, prompt hashes, seed, costs, latency, failure modes, and
uncertainty are recorded. Model self-confidence is not calibrated probability.
Report null and negative results and preserve the distinction between concise
rationale/evidence and private hidden reasoning.

Any implementation technology should be selected after the protocol contract
is stable. A minimal Python package with JSON-Schema validation is a reasonable
first slice, but is not a current repository fact.

