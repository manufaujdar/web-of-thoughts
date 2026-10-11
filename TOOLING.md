# Repository quality checks

Developer tooling checks the code and run-record structure. It does not establish scientific superiority, authorize experiments or call a model provider. The [quality runner](tools/quality.py), [native hook](.githooks/pre-push) and [main CI](.github/workflows/validate.yml) share the declared checks.

## Setup

Use Python 3.12 and Node 24. Install the existing Python development dependencies into `.venv` and run `npm ci --prefix frontend`. Run `npm --prefix frontend exec playwright install chromium` for local browser checks. The Python dispatcher uses `.venv/bin/python` when available.

The portfolio workstation installer supplies Betterleaks 1.8.1, Lychee 0.24.2, actionlint 1.7.12 and zizmor 1.30.1 on PATH. Frontend dev dependencies pin Playwright 1.64.0, axe integration 4.13.0 and Knip 6.41.0. The isolated tools/docs package pins markdownlint-cli 0.49.1 and patched transitive versions. Run `npm ci --prefix tools/docs` for the separate patched documentation lock. No provider key is needed for these checks.

## Checks

- `python3 tools/quality.py`: scoped docs/workflow checks, offline redacted secrets, the existing repository/schema validator, Python tests/compilation, frontend unit tests/build and synthetic browser checks.
- `python3 tools/quality.py --docs --base <full-before-push-sha>`: tooling documentation and changed canonical Markdown, offline local links/fragments, actionlint and offline zizmor. Historical documents are not blanket reformatted.
- `python3 tools/quality.py --advisory`: configured Knip report, without deleting code or presenting an advisory success as zero findings.
- `npm --prefix frontend run test:browser`: the actual built inquiry/workspace UI with every API route intercepted using synthetic records. It tests keyboard reading controls, browser persistence and stale-readable/quota-failure remount behavior; axe scans the expanded controls. It does not certify live SSE/provider behavior, every route or screen readers.

The existing Python repository validator retains run schema, vocabulary, budgets and privacy boundaries. Generic Markdown tools supplement it. Lychee is offline; it does not send private links to a remote checker. Betterleaks is redacted and does not validate keys against external APIs; native pre-push supplies the outgoing commit range, while a standalone call scans the latest commit. New staged changes need their own redacted pre-commit scan.

## Direct-main publication

The repository-owned `.githooks/pre-push` requires main, exact outgoing HEAD, clean tracked source and a remote-main ancestor before invoking the full quality command. Install it by composing with existing hooks through the portfolio installer. The existing pinned CI runs on main and also includes frontend unit tests and browser checks. Local hooks cannot prove every Git client is protected; hosted checks run after a direct-main push has landed.

The public repository also has pinned CodeQL source analysis for Python and JavaScript/TypeScript on main. It uses static extraction without building or executing the application, publishes findings to GitHub code scanning and makes no model-provider call. This does not establish clinical or scientific validity. No paid private-repository code-security entitlement is assumed for other portfolio projects.

Real-provider smoke remains separately required when a key and execution authorization are available. It is not silently simulated by this gate. Existing dependency advisories, experiment evidence and matched-budget evaluations remain visible. Roll back tooling by reverting its bounded commit and updating the local hook installation; preserve unrelated changes.

## Upstream

[Playwright accessibility guidance](https://playwright.dev/docs/accessibility-testing), [Knip CI guidance](https://knip.dev/guides/using-knip-in-ci), [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli), [Lychee](https://github.com/lycheeverse/lychee), [actionlint](https://github.com/rhysd/actionlint), [zizmor](https://github.com/zizmorcore/zizmor) and [Betterleaks](https://github.com/betterleaks/betterleaks) document the selected tooling. Optional external AI review is a separate manual action governed by privacy, account access and budget.

## Optional review scope

`python3 tools/coderabbit_review.py --base <full-before-push-sha>` prepares exact committed scope without calling a model. The manual CodeRabbit scope workflow also prepares only. External execution requires explicit authorization, authenticated CLI and agreed privacy/budget; no hook or push-triggered workflow calls an extra reviewer model.
