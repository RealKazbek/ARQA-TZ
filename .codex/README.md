# AI Agent Repository Guide

## Current technology map

- `frontend/`: React 18 single-page application built with Vite 5 and styled with Tailwind CSS. API calls are centralized in `frontend/src/api/client.js`.
- `backend/`: FastAPI application. `backend/main.py` currently defines HTTP routes and Pydantic request models; supporting data and batch-processing code lives in `backend/data/`.
- `drivepulse_stress_model/`: local Python stress-model training and inference pipeline.
- `earnings/earnings/`: local Python earnings-model training and inference pipeline.
- `tests/data/`: sample CSV fixtures. Do not assume a test runner is configured merely because test-like files exist.
- `docker-compose.yml`, `Dockerfile.backend`, `Dockerfile.frontend`, and `nginx.conf`: local containerized application setup.

The backend currently uses in-memory data stores. Do not introduce a database, cache, queue, remote service, or new deployment component unless the task explicitly requires it.

## Guidance index

- `architecture.md`: boundaries, imports, and where new code belongs.
- `coding-rules.md`: standards for Python, FastAPI, React, and shared code quality.
- `workflow.md`: mandatory inspection, validation, Git, and reporting sequence.
- `security.md`: secret handling, input validation, safe error handling, and dependency review.

When documentation and code disagree, inspect the code and configuration first, then update the relevant guidance only if the current task requires it.
