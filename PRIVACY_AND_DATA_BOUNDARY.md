# Privacy and data boundary

Status: experimental local research application. This file is a technical
privacy boundary, not a jurisdiction-specific privacy policy for a hosted
service.

## Current distribution

The bundled server is local-first, unauthenticated, and not approved for public
internet exposure. It can store local run metadata and event records under its
configured retention behavior. It must not receive credentials, personal or
regulated data, confidential prompts, private conversations, raw provider logs,
unlicensed artifacts, or hidden reasoning traces.

If the OpenAI or another provider adapter is enabled, prompts and outputs leave
the local process and are governed by the selected provider's current terms,
retention, training-use, region, and transfer settings. The repository does not
change those terms.

## Deployment responsibility

Before processing any personal or sensitive data, an operator must implement
authentication and ownership, authorization, rate/cost controls, prompt and
tool boundaries, encryption, retention/deletion, access/export handling,
provider review, incident response, and monitoring. The operator must publish
its own privacy notice and terms of service with the actual controller,
purposes, recipients, retention, rights, and transfers. This repository does
not provide those notices.

## Legal and research boundary

The Apache-2.0 `LICENSE` governs the source code. It does not grant rights to
provider services, models, datasets, prompts, outputs, or external references,
and it does not establish scientific validity or compliance. See `NOTICE`,
`docs/07-provenance.md`, `docs/09-application.md`, and `SECURITY.md`.

Reviewed: 2026-08-14.
