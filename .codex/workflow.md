# Required Workflow

Follow this sequence for every future implementation prompt.

1. Read `AGENTS.md` and the relevant files in `.codex/`.
2. Run `git status --short` and preserve unrelated user changes.
3. Inspect the relevant code, configuration, tests, and dependency relationships before editing.
4. Choose the smallest correct implementation plan. Ask only when a decision materially changes product behavior, causes destructive data loss, needs unavailable credentials, introduces a major architectural choice, or conflicts with requirements.
5. Implement only the requested work.
6. Review `git diff` for correctness, scope, secrets, and unintended formatting changes.
7. Run checks relevant to the changed area.
8. Fix failures caused by the change and rerun the affected checks.
9. Review `git status --short` and `git diff` again to ensure only intended files changed.
10. Create one or more logical commits.
11. Verify the current branch and target remote, then push completed commits unless the user explicitly says not to.
12. Provide the concise completion report described below.

## Validation guidance

Use checks that exist in this repository and are relevant to the change. Typical examples include:

- Frontend build: `npm --prefix frontend run build`
- Python syntax check for changed Python modules: `python -m compileall <changed paths>`
- Model pipeline checks when their code changes, such as the relevant `run.py` or `test_model.py` command after inspecting its supported options
- Container configuration review: `docker compose config`

Do not claim checks passed unless they ran successfully. If a required check is unavailable or an unrelated pre-existing failure blocks it, say so clearly. Do not commit knowingly broken work or push changes that fail required checks because of the change.

## Git rules

- Commit and push every successfully completed future prompt automatically unless the user explicitly says not to.
- Before committing, run `git status --short`, inspect `git diff`, and run relevant checks.
- Use logical commit boundaries: a small atomic task is usually one commit; independent logical changes may use multiple commits.
- Prefer Conventional Commit prefixes: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`, `build:`, or `ci:`.
- Use meaningful messages. Never use vague messages such as `update`, `changes`, `fix stuff`, `final`, `work`, or `commit 1`.
- Never commit secrets. Never force-push or rewrite published history. Never use `git reset --hard` unless the user explicitly authorizes it.

## Completion report

Report only:

- **Implemented:** important changes.
- **Validation:** commands/checks and their results.
- **Git:** commit hash(es), messages, branch, and push status.
- **Notes:** only material limitations or follow-up items.
