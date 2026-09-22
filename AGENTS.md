# Working in seebirds-app

## Project and priorities
- This repository is mcxvio/seebirds-app, the Python/Flask eBird application. It is distinct from the seebirds blog.
- Work in this order: get the existing application running; assess and agree baseline stack improvements; add features.
- Keep changes scoped to the current Linear issue. Do not combine startup fixes with an unsolicited rewrite or dependency modernization.

## Delivery workflow
- ChatGPT and Marcus agree scope; Linear holds the task, context, boundaries and acceptance criteria; Codex implements and validates; GitHub hosts the pull request; Marcus reviews and merges.
- Every repository change must be tracked by a Linear issue in the seebirds-app project.
- Inspect the repository instructions and current source before editing. Confirm the repository identity and base commit; target main unless the issue specifies otherwise.
- Implement on a task branch, include the Linear issue identifier in the branch and PR title, and link the Linear issue in the PR body.
- Commit the scoped changes and create the GitHub PR directly using supported authenticated tools or Codex publication facilities when available. Do not stop at a local diff if PR publication is available.
- Do not push directly to main, merge, enable auto-merge or deploy unless Marcus explicitly authorizes that action.
- Report the result in the originating Linear issue/session: summary, validation commands and results, remaining limitations, commit SHA, and actual GitHub PR URL and target branch.
- Verify the PR exists and the Linear link is present. Distinguish a local commit, a published branch and a published PR. Never claim publication, CI success, merge or deployment without evidence.
- If publication is unavailable, preserve the completed change, report the exact blocker and identify the remaining handoff. Never invent a PR URL or request credentials be pasted into an issue.

## Task sizing and decisions
- Follow the adopted process inspired by Matt Pocock's /to-spec and /to-tickets: start with the thinnest independently demonstrable working path and expand in small coherent changes.
- Use one self-contained issue when there is one clear outcome, one coherent PR and acceptance criteria fit in the issue.
- Use a Linear project specification plus smaller tracer-bullet issues for three or more independently useful changes, or two changes with significant shared decisions.
- When the approach is uncertain, start with a bounded assessment rather than speculative implementation.
- Each implementation issue must have a demonstrable outcome and proportionate validation.
- Record agreed durable owner/architecture decisions in decisions.md when relevant; keep project specifications in Linear and link them. Do not invent owner decisions or assume external skills are installed.

## Repository orientation
- app.py: Flask entry point and routes.
- apis/ebird/: eBird requests, data formatting and search history.
- templates/ and static/: server-rendered interface and assets.
- tests/: Python tests; static/tests/jasmine/: browser-side tests.
- requirements.txt: Python dependencies.
- dockerfile, docker-compose.yml and uwsgi.ini: existing container/server setup.
- README.md and azure-pipelines.yml contain historical infrastructure assumptions; verify them before using them as current deployment instructions.

## Configuration and secrets
- app.cfg is local configuration used at application import; it supplies SECRET_KEY and DAYS_BACK.
- keys.json supplies ebird_key / X-eBirdApiToken for eBird-backed functionality.
- Never commit real configuration secrets or print tokens, secret keys or credential files in logs, test output, PRs or Linear.
- Obtain required configuration through the approved environment/secret mechanism. Report missing names without revealing values. Do not fabricate production credentials.
- Missing runtime configuration does not block documentation-only work.
- Inspect live API tests before running them: the existing API suite includes token-printing behavior. Do not run it with real credentials until that behavior is removed in a scoped change.
- Prefer offline checks and mocked external services. Run live eBird calls only when the task authorizes them.

## Validation
- Choose checks proportional to the change and report what actually ran. Do not add tests that merely mirror documentation or implementation.
- For documentation-only changes, review accuracy and scope and run git diff --check; application startup and real secrets are not required.
- For Python changes, syntax checks and the offline data tests are useful starting points:
  - python3 -m compileall -q app.py apis tests
  - python3 -m unittest -v tests/test_ebird_json.py
- These checks do not prove that the application starts or that eBird integration works. Validate affected behavior separately when configuration and scope permit.
- Existing Flask session tests were found to use session outside a request context; distinguish existing failures from regressions and fix only within agreed scope.
- Dependency versions, network access, Docker availability and CI must be checked in the active environment. Do not assume that local tool availability or a successful local check means GitHub CI passed.
