# Coding Rules

## General

- Use names that communicate intent. Give each function one clear responsibility.
- Prefer small, direct changes and existing patterns over clever abstractions.
- Eliminate duplication when it is real and local enough to justify a shared helper; do not abstract hypothetical reuse.
- Avoid dead code, unused imports/dependencies, magic values without context, placeholder implementations, temporary debugging output, and unexplained TODOs.
- Comments should explain non-obvious reasoning or constraints, not narrate syntax. Do not generate verbose AI-style comments.
- Never leave commented-out code. Delete it or retain it in Git history.

## Frontend

- Build understandable, focused React components; split oversized components by responsibility.
- Keep calculations and business rules out of components. Use API/client or domain helpers where appropriate.
- Do not duplicate server/API state unnecessarily.
- Make user-facing interactions accessible and responsive: use semantic controls, usable labels, keyboard-friendly flows, and states that work at narrow viewport widths.
- Every asynchronous flow must deliberately handle loading, success, empty, and error states.
- Do not add UI libraries or replace the current frontend stack unless needed by the assigned task.

## Backend and Python

- Model external request payloads explicitly with Pydantic where appropriate, and validate uploaded CSV/content before processing it.
- Keep HTTP-specific concerns in route handlers and reusable business/data logic outside them where practical.
- Use appropriate HTTP status codes and stable, useful client-facing errors. Do not leak internal exceptions, stack traces, filesystem paths, secrets, or implementation details.
- Do not silently coerce or ignore invalid data. Return or raise a clear validation error.
- Preserve deterministic behavior where reasonable, especially for data transformation and model-related code.

## Tests

- Every behavior change needs proportionate verification. Add or update tests for business logic; for bug fixes, prefer a regression test.
- Test observable behavior instead of internal implementation details.
- Do not alter, delete, or weaken tests merely to make incorrect code pass.
- The repository currently has no configured frontend `test`, `lint`, or type-check npm script. Do not invent scripts as a workaround; run the checks actually available and report any gap.
