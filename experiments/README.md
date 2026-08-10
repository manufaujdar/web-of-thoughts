# Experiments

Keep each experiment in `experiments/YYYY-MM-DD-short-name/` with:

```text
protocol.md       preregistered question, task set, budgets, and metrics
runs/             one JSON record per run
outputs/          raw model outputs or references to immutable storage
analysis/         scripts or notebooks
report.md         results, uncertainty, failures, and interpretation
```

Do not overwrite completed runs. Corrections should create a new run and link the invalidated one.

Run `python3 tools/validate_repository.py` before review. A schema-valid run is structurally admissible only; it is not automatically fair, reproducible, or scientifically valid.

## Naming

Use run IDs such as:

`<task>-<method>-<model>-<seed>-<attempt>`

Hash or version every prompt. Record model identifier, date, sampling parameters, tool access, retries, and actual usage.

## Minimum report

- research question and falsifiable hypothesis;
- task inclusion/exclusion rules;
- baseline and WoT configurations;
- planned and actual sample sizes;
- primary and secondary metrics;
- quality–cost–latency table;
- uncertainty or variance;
- invalid and failed runs;
- qualitative failure examples;
- deviations from protocol;
- conclusion bounded to tested tasks and models.

## Safety and provenance

Use synthetic or explicitly redistributable tasks by default. Add model and dataset/task-set cards from `templates/` when external systems or data are introduced. Never store credentials, personal or regulated data, proprietary prompts, private hidden reasoning, restricted benchmark content, or raw provider logs in run artifacts.

Label reports as `illustrative`, `pilot`, `confirmatory`, or `replicated` according to `docs/07-provenance.md`. Examples and fixtures are not evidence.
