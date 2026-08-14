# Provenance and reproducibility

## Required provenance

Every substantive experiment should record:

- repository commit and specification version;
- complete prompt files or immutable hashes;
- task source, license, version, split, and transformations;
- model provider, exact identifier, access date, parameters, and seed support;
- tools, retrieval sources, evaluator, and verifier versions;
- actual calls, tokens, tool use, latency, and cost;
- exclusions, retries, failures, and protocol deviations;
- hardware and software environment when local execution can affect results.

## Third-party material

Do not copy benchmarks, prompts, datasets, outputs, or code into the repository solely because they are publicly accessible. Record the original source, license, modifications, and redistribution permission. Link to material when redistribution is unclear.

Generated outputs must identify the generating system and relevant parameters. Human edits should be disclosed when they affect evaluation.

## Evidence levels

- `illustrative`: an example that demonstrates format or mechanics;
- `pilot`: exploratory evidence used to refine the protocol;
- `confirmatory`: produced under a frozen protocol on held-out tasks;
- `replicated`: independently reproduced on a second implementation or model family.

Reports must not promote evidence to a higher level based on presentation quality or schema completeness.

## Artifact retention

Prefer small, reviewable records. Large or restricted artifacts should live in immutable, access-controlled storage with checksums and retention rules; commit only a manifest. Remove secrets and personal information before preservation.
