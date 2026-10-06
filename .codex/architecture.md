# Architecture Rules

## Boundaries

Keep these concerns separate:

- Frontend presentation and UI state: `frontend/src/pages/` and `frontend/src/components/`.
- Frontend HTTP access: `frontend/src/api/client.js` and narrowly related API helpers.
- Backend HTTP contracts: FastAPI routes and Pydantic models in `backend/`.
- Backend domain and data operations: focused modules under `backend/data/` or another clearly named domain module when a new domain warrants it.
- ML feature engineering, training, and inference: their respective local model directories.
- Test fixtures and tests: `tests/` and frontend test directories when a runner is configured.
- Runtime/configuration: dependency manifests, Docker files, Compose, Vite, Tailwind, and Nginx configuration.

## Implementation rules

- Keep API handlers thin: validate/parse request data, call focused logic, and return an explicit response.
- Put reusable calculations and business rules in dedicated Python modules, never in React components or duplicated route handlers.
- Validate at boundaries: incoming HTTP data, CSV uploads, environment configuration, and model input contracts.
- Preserve clear dependency direction: UI → API client → HTTP API → domain/data/model logic. Do not create circular imports.
- Prefer direct, focused modules over wrapper layers. Do not create repositories, factories, managers, adapters, providers, or interfaces without a present project need.
- Avoid giant files. Split only when it produces a clearer responsibility, not for ceremony.
- Treat model artifacts and feature-contract files as coupled to their corresponding inference code. Do not change them casually or regenerate them without task authorization.

## Current constraints

- The frontend stack is React/Vite/Tailwind; do not replace it without explicit instruction.
- The backend stack is FastAPI/Pydantic/Uvicorn; do not replace it without explicit instruction.
- The application is configured for local Docker Compose execution. Keep local development straightforward and deterministic.
- Existing code may be removed by future tasks when it is obsolete, but inspect callers and dependencies before doing so. Do not retain legacy code merely because it exists.
