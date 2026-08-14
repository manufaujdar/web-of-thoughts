# Governance

## Project status

Web of Thoughts is an early experimental specification. Maintainers steward the repository; acceptance of a contribution does not validate a method or establish scientific consensus.

## Decision classes

- **Editorial changes** may be accepted through ordinary review.
- **Implementation and tooling changes** require tests and documented compatibility impact.
- **Protocol changes**—hypotheses, task populations, baselines, budgets, operators, stopping rules, exclusions, or metrics—must follow the experiment-design process in `AGENTS.md` and be versioned before results are inspected.
- **Scientific claims** require reproducible, budget-matched evidence and an independent audit. Schema validity alone is insufficient.
- **Breaking changes** require a migration note and version change.

## Roles

- Maintainers merge changes, manage releases, enforce community standards, and resolve security reports.
- Contributors propose changes and supply evidence appropriate to the decision class.
- Experiment designers predeclare comparisons and validity conditions.
- Independent reviewers audit claims and must not be represented as independent when they authored the implementation or analysis under review.

## Decision record

Decisions should be visible in pull requests, protocol documents, experiment reports, or release notes. If consensus is not possible, maintainers decide and record the rationale, alternatives, conflicts of interest, and conditions for revisiting the decision.

## Releases

A release must identify the specification version, commit, prompt hashes where relevant, schema compatibility, validation status, known limitations, and evidence level. Releases must not imply general WoT superiority without qualifying empirical support.

## Conflicts and appeals

Disclose financial, professional, benchmark, model-provider, or authorship interests that could affect a review. Appeals should present new evidence or a process failure and may request a different reviewer when feasible.
