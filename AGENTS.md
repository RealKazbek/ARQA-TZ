# AI Agent Instructions

These instructions apply to Codex and every other AI coding agent working in this repository. They are repository-wide and take precedence over convenience or speculative improvements.

Start every task by reading this file and the relevant guidance in [`.codex/`](.codex/):

- [`.codex/README.md`](.codex/README.md) — repository map and documentation index
- [`.codex/architecture.md`](.codex/architecture.md) — boundaries and current stack
- [`.codex/coding-rules.md`](.codex/coding-rules.md) — implementation standards
- [`.codex/workflow.md`](.codex/workflow.md) — required task and Git workflow
- [`.codex/security.md`](.codex/security.md) — security and dependency rules

The project must stay simple, readable, maintainable, secure, deterministic, easy to review, and easy to run locally. Prefer boring, reliable engineering. Do not add complexity, dependencies, infrastructure, patterns, abstractions, or product behavior unless the current task requires them.

Before editing, inspect the existing implementation, its dependencies, and its relevant established patterns. Reuse suitable code; do not duplicate logic. Existing open-source-derived code is not automatically permanent: preserve it only when it remains relevant, and remove obsolete code cleanly when a task calls for removal. Never keep dead or commented-out implementations. Do not remove license or attribution files without explicit instruction.

Keep all work within the requested scope. Do not redesign the application, refactor unrelated code, rename unrelated files, reformat the whole repository, or change unrelated configuration. Report unrelated issues instead of silently expanding scope.

For every completed implementation task, follow the complete workflow in [`.codex/workflow.md`](.codex/workflow.md): inspect status and code, make the smallest correct change, review the diff, run relevant checks, commit logical changes, and push them to the configured remote branch unless the user explicitly says not to.
