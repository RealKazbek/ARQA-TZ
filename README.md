# Driver Shift Diary — ARQA Technical Assignment

A small web application for reviewing a driver's trips and earnings for a selected day. The client shows the daily diary; the API provides daily data and retry-safe trip creation.

## Stack

- React, TypeScript, Vite, and Tailwind CSS
- FastAPI and Pydantic
- JSON-file storage

## Quick Start

With Docker available, start the whole application from the repository root:

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/api/health

### Without Docker

In one terminal:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r backend/requirements.txt -r backend/requirements-dev.txt
python3 -m uvicorn backend.main:app --reload
```

In another terminal:

```bash
npm --prefix frontend install
npm --prefix frontend run dev
```

The same URLs above apply. The frontend development server proxies `/api` requests to the backend.

## Quick Verification

### 1. Check the daily diary

Open the frontend and select **2026-10-01**. It is also the initial date in the committed demo data.

Additional demo shifts are available on 2026-10-02 through 2026-10-04 for date-switching demonstration.

Expected values:

| Metric | Value |
| --- | ---: |
| Trips | 2 |
| Revenue | 3 900 ₸ |
| Commission | 585 ₸ |
| Net earnings | 3 315 ₸ |
| Cash | 1 500 ₸ |
| Card | 2 400 ₸ |

### 2. Check date switching

Use the previous/next controls or date input. The client requests `GET /api/trips?date=YYYY-MM-DD` for the selected day and shows that day's summary and trips. A day with no trips is an expected empty state.

### 3. Check trip creation and idempotency

Open Swagger at http://localhost:8000/docs, expand `POST /api/trips`, click **Try it out**, and submit:

```json
{
  "id": "review-1",
  "start": "2026-10-02T10:00:00+05:00",
  "end": "2026-10-02T10:25:00+05:00",
  "amount": 2000,
  "payment": "card",
  "commission": 300
}
```

- First request: `201 Created`
- Send the identical request again: `200 OK`; only one trip is stored
- Send the same `id` with any changed field: `409 Conflict`

Then retrieve `GET /api/trips?date=2026-10-02` to see the single created trip and its summary.

### 4. Check validation

`amount <= 0` is rejected, as is `end <= start`. Invalid requests are not written to storage.

### 5. Run tests

After installing the Python dependencies above, run the complete backend suite:

```bash
python3 -m unittest discover -s tests -v
```

## Requirements Matrix

| ARQA requirement | Implementation |
| --- | --- |
| Daily trips API | `GET /api/trips?date=YYYY-MM-DD` |
| Daily summary | Backend calculates count, revenue, commission, net, cash, and card totals |
| Day switching | Frontend date controls fetch the selected day |
| POST trip | `POST /api/trips` persists a valid JSON trip |
| Validation | Positive amount and end-after-start validation via Pydantic |
| Duplicate protection | Client-provided trip ID; identical retry returns `200`, conflicting reuse returns `409` |
| Summary tests | `tests/test_trip_domain.py` |
| Duplicate tests | `tests/test_trip_api.py` |

## Architecture

The React/Vite client displays data from the FastAPI server. The server reads and writes `backend/data/trips.json`; daily financial calculations stay in backend domain code rather than the UI.

Trips belong to the calendar day of their offset-aware `start` timestamp. Amounts are stored and calculated as integer tenge values.

## API Examples

```bash
curl 'http://localhost:8000/api/trips?date=2026-10-01'
```

```bash
curl -X POST http://localhost:8000/api/trips \
  -H 'Content-Type: application/json' \
  -d '{"id":"review-1","start":"2026-10-02T10:00:00+05:00","end":"2026-10-02T10:25:00+05:00","amount":2000,"payment":"card","commission":300}'
```

For the interactive API contract and request example, use Swagger at http://localhost:8000/docs.

## Render Deployment

Create two services from the `RealKazbek/ARQA-TZ` repository.

### Backend

- Service type: **Web Service** with the Docker runtime.
- Root directory: `/backend`; Render detects `Dockerfile` there.
- Build command: none; the Dockerfile installs `requirements.txt`.
- Start command: none; the Dockerfile runs Uvicorn on `0.0.0.0:$PORT`.
- Set healthcheck path to `/api/health`, then use the generated public backend URL for the API and Swagger.
- After generating the frontend domain, set `FRONTEND_ORIGIN=https://<frontend-domain>.onrender.com`.

`TRIPS_FILE_PATH` remains optional and defaults to the committed `backend/data/trips.json` dataset. Do not configure a persistent disk for the free demo.

### Frontend

- Service type: **Static Site**.
- Root directory: `/frontend`.
- Build command: `npm ci && npm run build`.
- Publish directory: `dist`.
- Set the build variable `VITE_API_URL=https://<backend-domain>.onrender.com`.

The frontend uses `VITE_API_URL` in production. Local Vite and Docker Compose leave it empty and continue to use their existing `/api` proxy.

Render Free Web Service storage is ephemeral. A fresh deployment starts from the committed demo dataset; trips created with `POST /api/trips` are not guaranteed to survive redeploys.

## AI Usage

AI/Codex was used for repository analysis, scoped cleanup/refactoring assistance, implementation assistance, and test generation/review. A concrete AI-assisted analysis mistake was initially treating parts of the legacy Driver Pulse application as candidates for reuse; manual review corrected that direction and removed its unrelated ML, stress, map, goal, and dashboard scope. The implementation also deliberately uses the client-supplied stable trip ID for idempotency rather than a fragile heuristic based on timestamps or amounts, and keeps financial calculations in the backend using integer tenge values.
