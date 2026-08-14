# Software architecture

Web of Thoughts currently consists of a versioned research specification and
experiment-record contract rather than a production inference service.

## Conceptual flow

Task framing -> dimension selection -> seed thoughts -> expansion -> typed links
-> challenge/verification -> synthesis -> selection -> stopping -> run record.

The formal web state contains nodes, typed edges, dimensions, frontier
operations, an assumption/constraint ledger, and a remaining budget vector.

## Repository components

- docs/: conceptual, formal, protocol, landscape, evaluation, roadmap, and glossary contracts.
- prompts/: modular controller, node-generator, evaluator, synthesizer, and finalizer prompts.
- schemas/run.schema.json: JSON Schema for experiment records.
- experiments/: naming, run template, and reporting conventions.
- .agents/skills: experiment-design and audit workflows.
- .ai/: project context, memory, team, and handoff.

There is no committed runtime package, API server, database, or provider adapter
in the current tree. An eventual runner should be a separate implementation
that consumes these versioned contracts.

## Trust boundary

Run records should preserve provider/model version, budgets, prompt hashes,
usage, result status, termination reason, evidence, and costs without storing
private hidden reasoning traces or sensitive raw task data. Claims must be
auditable from the concise record and external evidence.

