# Driver Shift Diary

This repository is being prepared for the ARQA technical assignment.

The current revision contains a minimal React/Vite frontend, a read-only FastAPI trip endpoint, JSON trip storage, and daily summary calculations. Trip creation, duplicate handling, and the final UI are intentionally deferred to subsequent implementation phases.

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn backend.main:app --reload
```

In another terminal:

```bash
npm --prefix frontend install
npm --prefix frontend run dev
```

The backend health endpoint is available at `http://localhost:8000/api/health`.
