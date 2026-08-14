# Research and deployment boundaries

## Current evidence level

Web of Thoughts has a functional research-prototype controller and local application, but remains at Phase-0 evidence. The repository contains no completed benchmark suite, validated controller, trained model, production service, or evidence that WoT generally outperforms direct prompting, Chain of Thought, Tree of Thoughts, or Graph of Thoughts.

Prompts and formulas are hypotheses. Self-evaluation scores are routing heuristics, not calibrated probabilities or proof of correctness.

## Appropriate use

The repository is suitable for controlled experiments, prompt and controller prototyping, live local demonstrations with non-sensitive content, reproducibility studies, and analysis of quality–cost tradeoffs using checkable or blindly evaluated tasks.

## Unsupported use

Do not represent the current framework as:

- a validated general reasoning improvement;
- a source of diagnosis, legal judgment, financial suitability, or safety-critical authorization;
- a substitute for domain experts, authoritative sources, deterministic checks, or human accountability;
- a method for revealing or storing private hidden chain-of-thought;
- a security, privacy, factuality, or alignment guarantee;
- a production-ready autonomous agent architecture.

High-impact use requires domain-specific validation, human oversight, fail-safe behavior, incident response, monitoring, rollback, privacy review, and applicable legal or regulatory review outside this project.

## Data and privacy

Use synthetic or redistributable data by default. Collect the least information needed for the experiment. Keep raw prompts and outputs local unless participants and data owners have authorized storage and redistribution. Treat model-provider retention and training policies as part of the experiment environment.

Never preserve hidden reasoning traces. Record concise decision artifacts, evidence, verifier outcomes, budgets, and uncertainty as defined by the protocol.

## External models and tools

Models, search systems, evaluators, and tools can change without notice. Record provider, exact model identifier, date, parameters, tool access, retries, and observed usage. Treat remote output as untrusted and independently verify consequential claims.

## Requirements before broader deployment

- repeatable benefits on declared task populations and multiple model families;
- strong budget-matched baselines and required ablations;
- independent audit and evaluator-bias analysis;
- privacy, security, abuse, and prompt-injection threat models;
- task-specific acceptance and safe-failure criteria;
- complete data, model, prompt, and dependency provenance;
- monitoring for accuracy, cost, latency, drift, and failure modes;
- rollback and incident-response procedures;
- explicit human ownership of final decisions.
