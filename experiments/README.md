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

