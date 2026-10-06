# Driver Shift Diary

This repository is being prepared for the ARQA technical assignment.

The current revision contains a React/Vite shift-diary interface, FastAPI trip endpoints, JSON trip storage, and daily summary calculations. The frontend displays backend-provided trip and summary data for a selected day.

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
