# Documentation index

Web of Thoughts is an experimental, typed, budget-aware graph reasoning
framework. Its working application does not establish superiority over direct
prompting, chains or trees.

## Find the right document

| Task | Read |
| --- | --- |
| Run the local application | [Root README](../README.md) and [application guide](09-application.md) |
| Understand the method | [Concept](00-concept.md), [formal model](01-formal-model.md), [protocol](02-protocol.md) and [glossary](glossary.md) |
| Design or evaluate an experiment | [Evaluation](04-evaluation.md), [research landscape](03-research-landscape.md) and [experiment conventions](../experiments/README.md) |
| Understand runtime boundaries | [Architecture](architecture.md) and [technical overview](technical-overview.md) |
| Validate a change or prepare a release | [Validation protocol](08-validation-protocol.md), [contributing](../CONTRIBUTING.md) and [tooling](../TOOLING.md) |
| Check data, model or license conditions | [Research boundaries](06-research-boundaries.md), [provenance](07-provenance.md), [security](../SECURITY.md) and [license](../LICENSE) |
| Select the next research step | [Roadmap](05-roadmap.md); experiment records remain authoritative for results |
| Resume agent work | [Agent guide](../AGENTS.md), [team](../.ai/TEAM.md) and [active handoff](../.ai/HANDOFF.md) |

## File placement

| Location | Purpose |
| --- | --- |
| `docs/` | Numbered method/evaluation guides and software explanations |
| `prompts/` | Versioned modular prompt components |
| `schemas/` | Machine-readable experiment record contract |
| `experiments/` | Run templates, records and analysis conventions |
| `templates/` | Model and dataset provenance cards |
| `wot_app/`, `frontend/` | Backend and React workbench source |
| `tests/`, `tools/` | Synthetic tests, structural validation and maintenance |
| `.ai/`, `.agents/` | Project continuity and bounded role instructions |

Keep run evidence with its experiment instead of creating competing results
summaries. Preserve concise rationale, evidence, decisions, budgets and outcomes;
private hidden reasoning is not a repository artifact. Apache-2.0 covers the
repository source; provider, benchmark and external-data terms remain separate.
