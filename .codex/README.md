# AI Agent Repository Guide

## Current technology map

- `frontend/`: React 18 single-page application built with Vite 5 and styled with Tailwind CSS.
- `backend/`: minimal FastAPI application. `backend/main.py` currently exposes only an operational health endpoint.
- `tests/`: reserved for the focused automated test suite added in a later phase.
- `docker-compose.yml`, `Dockerfile.backend`, `Dockerfile.frontend`, and `nginx.conf`: local containerized application setup.

The repository intentionally has no trip domain or storage implementation yet. Do not introduce a database, cache, queue, remote service, or new deployment component unless the task explicitly requires it.

## Guidance index

- `architecture.md`: boundaries, imports, and where new code belongs.
- `coding-rules.md`: standards for Python, FastAPI, React, and shared code quality.
- `workflow.md`: mandatory inspection, validation, Git, and reporting sequence.
- `security.md`: secret handling, input validation, safe error handling, and dependency review.

When documentation and code disagree, inspect the code and configuration first, then update the relevant guidance only if the current task requires it.
