# AI Agent Repository Guide

## Current technology map

- `frontend/`: React 18 TypeScript single-page application built with Vite 5 and styled with Tailwind CSS. It contains the ARQA daily shift-diary view and a small API layer under `src/api/`.
- `backend/`: FastAPI application with a read-only daily trips endpoint. Trip models and summary calculation live in `backend/trips.py`; JSON persistence lives in `backend/storage.py`.
- `backend/data/trips.json`: small ARQA-format sample data set and repository-local storage location.
- `tests/`: focused backend and API tests for summary, storage, creation, validation, and retry behavior. `requirements-dev.txt` supplies the API test client dependency.
- `docker-compose.yml`, `Dockerfile.backend`, `Dockerfile.frontend`, and `nginx.conf`: local containerized application setup.

The repository uses a concrete JSON file, not a database. Do not introduce a database, cache, queue, remote service, or new deployment component unless the task explicitly requires it.

## Guidance index

- `architecture.md`: boundaries, imports, and where new code belongs.
- `coding-rules.md`: standards for Python, FastAPI, React, and shared code quality.
- `workflow.md`: mandatory inspection, validation, Git, and reporting sequence.
- `security.md`: secret handling, input validation, safe error handling, and dependency review.

When documentation and code disagree, inspect the code and configuration first, then update the relevant guidance only if the current task requires it.
