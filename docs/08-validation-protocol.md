# Validation protocol

Repository checks prevent malformed artifacts and unsupported release mechanics; they do not validate WoT's scientific claims.

## Local checks

Run from the repository root:

```bash
python3 tools/validate_repository.py
python3 -m unittest discover -s tests -v
python3 -m compileall -q wot_app tools tests
npm ci --prefix frontend
npm run build --prefix frontend
git diff --check
```

The validator checks required community files, parses the run schema, checks local Markdown links, flags likely sensitive tracked paths, and validates committed run JSON files. Full JSON Schema validation uses the optional `jsonschema` development dependency; deterministic core checks remain available without it.

Application releases should also run `python3 tools/live_smoke.py` with a dedicated, budget-limited OpenAI API key. That test incurs API cost and must be reported as not run—not passed—when no key is available.

## Experiment gates

A run is structurally admissible only when:

- its JSON is schema-valid;
- its actual usage does not exceed the declared budget without an explicit invalid status;
- the method, model, prompt hashes, termination reason, and result status are recorded;
- artifacts do not include private hidden reasoning or restricted data;
- failed, partial, and excluded runs remain visible.

Admissibility does not imply fairness or scientific validity. A comparison also needs frozen metrics, matched access and budgets, leakage review, independent outcome checks, uncertainty, and documented deviations.

## Release gates

- all local and CI checks pass on the release commit;
- license, notice, citation, governance, security, and boundary documents are present;
- version and schema compatibility are documented;
- evidence claims match their declared evidence level;
- known failures and null results are included;
- no credentials, restricted data, or unverified weights are included.
