# Contributing

Web of Thoughts should evolve through explicit claims and reproducible evidence.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md). Security issues and exposed sensitive material must follow [SECURITY.md](SECURITY.md), not public issue discussion.

## Before opening a change

1. Read `AGENTS.md`, the research boundaries, and the smallest relevant protocol or prior experiment.
2. Classify the change as editorial, tooling, protocol, experiment/claim, or governance/release.
3. For protocol or metric changes, freeze the design before inspecting confirmatory results.
4. Use synthetic or redistributable fixtures and record third-party provenance.
5. Keep changes focused and state compatibility or migration effects.

## Proposing a mechanism

An addition must state:

1. the failure mode it addresses;
2. the proposed mechanism;
3. why an existing operator cannot handle it;
4. expected quality benefit and resource cost;
5. a falsifiable prediction;
6. an ablation or comparison plan;
7. new risks or ways it can fail.

## Changing the specification

- Keep terminology consistent with the glossary.
- Label untested defaults as hypotheses.
- Update prompts, schema, and evaluation plan when a contract changes.
- Record breaking changes in a future changelog before implementation begins.
- Do not use benchmark anecdotes as general proof.

## Experiment review checklist

- Is the baseline strong and budget-matched?
- Is the outcome independently checkable or blindly judged?
- Are prompts, versions, seeds, failures, and actual costs recorded?
- Could answer length or formatting bias the evaluator?
- Is the conclusion narrower than or equal to the evidence?
- Are null and negative results retained?

## Required validation

Run:

```bash
python3 tools/validate_repository.py
python3 -m unittest discover -s tests -v
python3 -m compileall -q wot_app tools tests
npm ci --prefix frontend
npm run build --prefix frontend
git diff --check
```

If the change affects prompts, schema, models, datasets, or experiment configuration, also record version/hash changes and update the relevant card or protocol. Passing automation establishes structure only; scientific claims still require budget matching, leakage review, uncertainty, and independent audit.

## Data and artifact policy

Do not commit credentials, personal or regulated data, confidential prompts, private hidden reasoning, restricted datasets, raw provider logs, unverified model weights, or artifacts with unclear redistribution rights. See [the provenance policy](docs/07-provenance.md) for manifests and evidence levels.
