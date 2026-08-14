# Security policy

## Supported scope

The repository is a local-first research application with a FastAPI backend, React frontend, SQLite persistence, and OpenAI integration. There is no bundled authentication system, hosted service, or validated model release. Do not expose it to the public internet without adding deployment-specific authentication, ownership, rate/cost controls, encrypted storage, monitoring, and incident response. Security support applies to the current default branch.

## Report a vulnerability

Do not open a public issue for a suspected vulnerability, exposed credential, private dataset, or prompt-injection path involving confidential data. Contact the repository owner privately through the security-reporting options on their GitHub profile or repository Security tab when available.

Include the affected commit, reproduction steps, impact, and any safe mitigation. Do not include real credentials, personal data, proprietary prompts, or harmful payloads.

## Repository data boundary

Never commit:

- credentials, access tokens, API keys, session cookies, or `.env` files;
- personal, confidential, regulated, or proprietary source data;
- private conversations or hidden model reasoning traces;
- unlicensed benchmark data, model outputs, weights, or evaluation artifacts;
- raw provider logs that may contain user content or identifiers;
- generated artifacts whose provenance and redistribution rights are unknown.

Use synthetic or explicitly redistributable fixtures. Redact identifiers before creating an issue or test case.

## Prompt and agent risks

Prompt templates are untrusted text, not a security boundary. Anyone integrating WoT must independently handle prompt injection, tool authorization, data exfiltration, sandboxing, rate limits, budget exhaustion, unsafe actions, and untrusted model output. The repository's schemas and quality gates do not make model output safe or correct.

## Dependency policy

Core validation uses the Python standard library. The optional `jsonschema` development dependency is bounded by major version. Dependency updates require tests, provenance review, and least-privilege CI permissions.
