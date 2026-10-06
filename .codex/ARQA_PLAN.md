# ARQA Implementation Plan

Source of truth: [ARQA technical assignment](https://jobs.arqa.cc/#task), reviewed on 2026-10-06. This is a plan only; it does not authorize implementation.

## 1. Explicit assignment requirements

### Backend

- Build a small “Driver Shift Diary” application. Any stack is allowed; a web client plus server is an acceptable form.
- Provide an API that returns, for a selected day, the trip list and a daily summary.
- Provide an API to add a trip.

### Frontend

- Show the daily summary and trip list.
- Allow the user to switch days.

### Data and storage

- Use a JSON file containing driver trips. Each trip has: `id`, start time, end time, amount, payment method (`cash` or `card`), and commission.
- The supplied example uses ISO 8601 timestamps with offsets and integer tenge amounts.

### Validation and idempotency

- On trip creation, validate that the amount is greater than zero and the end is later than the start.
- Re-sending the same trip must not create a duplicate.

### Business calculations

- Daily summary contains: trip count, revenue, commission, “to driver” amount, and cash/card breakdown.

### Testing

- Include tests for daily-summary calculation and duplicate protection.

### Build/run and submission

- Submit a public GitHub or GitLab repository with a README explaining how to run it and what was completed.
- Optionally submit a demo link or screenshots.
- Include a short note explaining how AI was used, where it made a mistake, and what was corrected manually.

### Optional / not required

- Demo link or screenshots.
- The assignment permits and encourages AI tools; it does not require a particular stack, database, authentication, deployment platform, mobile app, or extra product features.

## 2. Current repository audit

### Runtime and structure

- `frontend/` is a React 18, Vite 5, Tailwind CSS SPA. It currently uses React Router, Lucide, Recharts, Leaflet, and date-fns.
- `backend/main.py` is a 340-line FastAPI application with Pydantic models and 25 routes.
- `backend/data/sample_data.py` generates random synthetic trips and keeps state in process memory. It supplies maps, sensor signals, stress events, dashboard metrics, and goals.
- `backend/data/batch_processor.py`, `drivepulse_stress_model/`, and `earnings/earnings/` implement unrelated ML prediction/training workflows.
- `streamlit_app.py` is a separate ML dashboard.
- Docker Compose builds an Nginx-served Vite frontend and a Python backend. The current backend image installs ML dependencies and copies model folders.
- `Procfile` and `vercel.json` are deployment-specific configuration. `README.md` documents Driver Pulse, not ARQA.

### Existing trip functionality

- `GET /api/trips` filters generated/in-memory Driver Pulse trips by date and several stress/earnings filters. It returns `{ trips, count }`, not an ARQA summary.
- `POST /api/trips` accepts `date`, time values, distance, fare, and optional stress score. It generates a UUID and accepts no payment method or commission.
- The create route checks only time order explicitly; it does not enforce ARQA amount rules reliably and has no duplicate protection.
- `frontend/src/pages/Trips.jsx` displays Driver Pulse trips, filters, CSV import, and an add-trip dialog. It has no commission/payment input or daily summary.
- `frontend/src/pages/Dashboard.jsx` has a two-day toggle but a Driver Pulse dashboard with goals and stress metrics, not the required selected-day summary.

### Tests and checks

- The two frontend files under `frontend/src/__tests__/` are illustrative exports/pseudo-tests. No npm test, lint, or type-check script is configured.
- There are CSV fixtures but no automated backend test suite or test runner configuration.
- `npm --prefix frontend run build` exists. Docker Compose is configured.

## 3. Gap analysis

| ARQA requirement | Status | Current state |
| --- | --- | --- |
| Server API returns selected-day trip list | PARTIAL | `GET /api/trips?date=` filters generated trips, but its schema and behavior are Driver Pulse-specific. |
| Server API returns daily summary | MISSING | Dashboard calculations omit commission, net, cash, and card totals. |
| Client shows summary and trip list | PARTIAL | Existing dashboard/trips pages show other summaries and trips but not ARQA data. |
| Client can switch days | PARTIAL | Date filtering/two-day controls exist but are hard-coded and not a coherent ARQA day selector. |
| JSON file of trips | MISSING | Data is generated in memory; existing files are ML CSV/artifacts. |
| Trip fields: id, start, end, amount, payment, commission | CONFLICTING | Existing trip shape uses `date`, `start_time`, `end_time`, `fare`, distance, stress, map, and events; it lacks payment and commission. |
| Create trip API | PARTIAL | A route exists but has the incompatible request/response schema. |
| Amount greater than zero | PARTIAL | UI attempts a generic money check, but the backend accepts `fare` without the ARQA `amount` contract or a strict positive constraint. |
| End later than start | PARTIAL | Backend checks the order, but uses a different payload and wraps errors broadly. |
| No duplicate after repeat submission | MISSING | Every request creates a new generated UUID and is inserted. |
| Trip count/revenue/commission/net/cash-card summary | MISSING | Only Driver Pulse fare/goal/stress calculations exist. |
| Tests for summary | MISSING | No runnable automated tests cover this. |
| Tests for duplicates | MISSING | No duplicate behavior or tests exist. |
| Public README with run instructions and completed work | PARTIAL | A README exists but describes the unrelated project. |
| Optional demo/screenshots | UNNECESSARY | A legacy live deployment exists but is not an ARQA demo and must not be represented as one. |
| AI usage note | MISSING | No ARQA-specific note exists. |

## 4. Keep, remove, and rewrite decisions

### Keep as is

- `.gitignore`, `AGENTS.md`, and repository-wide `.codex/` guidance.
- `frontend/package.json` tooling baseline: React, React DOM, Vite, Tailwind, PostCSS, Autoprefixer, and the Vite React plugin.
- `frontend/postcss.config.js` and `frontend/vite.config.js` proxy concept, subject to a small review when the final API path is fixed.
- `nginx.conf` reverse-proxy pattern, because `/api/` remains the client/server boundary.

### Keep and modify

- `backend/` package: retain it as the Python application location, but replace its Driver Pulse content with focused ARQA modules.
- `Dockerfile.backend`, `Dockerfile.frontend`, and `docker-compose.yml`: retain containerized local run support; simplify them after ML files/dependencies are removed.
- `frontend/index.html`, `frontend/src/index.css`, `frontend/src/main.jsx`, `frontend/src/App.jsx`, and `frontend/tailwind.config.js`: retain the Vite entry/build structure but remove Driver Pulse, Leaflet, and router-specific setup.
- `README.md`: replace it with the ARQA run guide, delivered features, API summary, test command, and concise AI-use note.
- `requirements.txt` and `backend/requirements.txt`: consolidate to only dependencies needed by the final FastAPI application; do not keep duplicate manifests without a concrete Docker/local need.
- `tests/`: retain the top-level location but replace CSV examples with focused automated tests.

### Rewrite

- `backend/main.py`: replace the 25-route Driver Pulse API with a small ARQA application entrypoint and only required HTTP routes.
- `frontend/src/api/client.js`: replace broad auth/dashboard/ML calls with a small trips API module.
- The frontend application: replace login, sidebar, dashboard, trips, and feature pages with a single accessible shift-diary view (summary, day control, trip list, and add-trip form).

### Remove in Phase 1 (exact current items)

**Directories**

- `drivepulse_stress_model/` (all calibration, data, model artifacts, source, README, requirements, and runner files).
- `earnings/` (including `earnings/__MACOSX/` and the complete nested earnings ML project).
- `docs/` (all legacy Driver Pulse progress/design/architecture assets).
- `frontend/src/__tests__/` (non-runnable Driver Pulse pseudo-tests).
- `tests/data/` (stress, earnings, and CSV import fixtures).

**Backend modules**

- `backend/agent.py`
- `backend/data/batch_processor.py`
- `backend/data/config.py`
- `backend/data/sample_data.py`
- `backend/data/trips_import.py`
- `backend/data/users.py`
- `backend/data/__init__.py`
- `backend/utils/logging.py`
- `backend/utils/__init__.py`

**Frontend pages/components/helpers**

- `frontend/src/pages/BatchUpload.jsx`
- `frontend/src/pages/Dashboard.jsx`
- `frontend/src/pages/Goals.jsx`
- `frontend/src/pages/Home.jsx`
- `frontend/src/pages/Predict.jsx`
- `frontend/src/pages/Trends.jsx`
- `frontend/src/pages/TripDetail.jsx`
- `frontend/src/pages/Trips.jsx`
- `frontend/src/components/AICopilot.jsx`
- `frontend/src/components/ConfidenceBadge.jsx`
- `frontend/src/components/EarningsProgress.jsx`
- `frontend/src/components/EventCard.jsx`
- `frontend/src/components/ExplainModal.jsx`
- `frontend/src/components/FeedbackButtons.jsx`
- `frontend/src/components/FilterChips.jsx`
- `frontend/src/components/Layout.jsx`
- `frontend/src/components/SampleTripCard.jsx`
- `frontend/src/components/Sidebar.jsx`
- `frontend/src/components/SignalCharts.jsx`
- `frontend/src/components/StressTips.jsx`
- `frontend/src/components/SummaryCard.jsx`
- `frontend/src/components/TimelineSlider.jsx`
- `frontend/src/components/TodayTimeline.jsx`
- `frontend/src/components/TripListItem.jsx`
- `frontend/src/components/TripMap.jsx`
- `frontend/src/utils/sanityChecks.js`
- `frontend/src/api/client.js`

**Entrypoints/configuration/assets**

- `streamlit_app.py`
- `Procfile`
- `vercel.json`
- root `package-lock.json` (there is no root `package.json`)

**Dependencies to remove in the future**

- Python: pandas, NumPy, scikit-learn, joblib, Streamlit, python-dateutil, python-multipart, google-generativeai, and python-dotenv.
- Frontend: react-router-dom, recharts, react-leaflet, leaflet, lucide-react, date-fns, and `@types/leaflet`.

Do not remove the listed material until Phase 1. No license or attribution file is currently present in the tracked repository.

## 5. Target architecture

Keep a small web application with a JSON file, not a database or external service:

```text
backend/
  app/
    main.py          # FastAPI application and thin routes
    schemas.py       # request/response models
    service.py       # validation-independent trip operations and summary calculation
    storage.py       # JSON-file read/write and ID lookup
  data/
    trips.json       # supplied/working trip data
  requirements.txt
tests/
  test_summary.py
  test_trip_api.py
frontend/
  src/
    api/trips.js
    components/      # day control, summary, list, creation form
    App.jsx
    main.jsx
    index.css
```

Use no authentication, users, database, cache, queue, background worker, WebSocket, global state framework, microservice, or cloud-only infrastructure. Keep the existing Vite dev proxy and Docker Compose deployment shape only because they make local execution simple.

## 6. Proposed API contract

The assignment does not prescribe endpoint paths or response envelopes; these are minimal implementation choices.

### `GET /api/trips?date=YYYY-MM-DD`

- Returns one selected calendar day based on each trip’s `start` timestamp.
- Response: `{ "date": "YYYY-MM-DD", "trips": [...], "summary": {...} }`.
- `trips` contains only ARQA trip fields: `id`, `start`, `end`, `amount`, `payment`, and `commission`.
- `summary` contains `trip_count`, `revenue`, `commission`, `net_amount`, `cash_amount`, and `card_amount`.
- Malformed/missing date receives a clear `422` validation response.

### `POST /api/trips`

- Request body: `{ "id", "start", "end", "amount", "payment", "commission" }`.
- `id` is required so the server has a stable identity for file-backed storage and repeat detection. `payment` is restricted to `cash` or `card`.
- First accepted request writes the trip and returns `201 Created` with the stored trip.
- An exact retry with an already stored `id` returns `200 OK` and the existing trip; it does not write a second record.
- A reused `id` with different values returns `409 Conflict`, preventing an ambiguous overwrite.
- Invalid body shape/timestamps/payment receives `422`; an amount not greater than zero or end not later than start receives `422` with a field-level message.

`GET /api/health` may remain as a non-product operational endpoint if Docker/local verification benefits from it; it is not an ARQA requirement and must not expand the UI.

## 7. Data model and calculations

### Trip

```json
{
  "id": "t1",
  "start": "2026-10-01T08:10:00+05:00",
  "end": "2026-10-01T08:32:00+05:00",
  "amount": 2400,
  "payment": "card",
  "commission": 360
}
```

The JSON file is the initial data source and storage for accepted additions. It must be read/write by the local backend. No persistence mechanism beyond that file is required by the assignment.

For selected-day trips `D` (where the local calendar date in `start` equals the requested day):

- `trip_count = count(D)`
- `revenue = sum(trip.amount for trip in D)`
- `commission = sum(trip.commission for trip in D)`
- `net_amount = revenue - commission`
- `cash_amount = sum(trip.amount for trip in D if trip.payment == "cash")`
- `card_amount = sum(trip.amount for trip in D if trip.payment == "card")`

The example proves the net formula: `3900 - 585 = 3315`. The assignment gives no commission-rate formula, rounding rule, currency-format rule, zero/negative commission rule, or rule for trips crossing midnight. Do not invent financial calculations. The implementation will preserve supplied monetary precision and calculate directly from stored values; the day assignment and cross-midnight behavior are recorded as an ambiguity below.

## 8. Idempotency strategy

- A trip’s client-supplied `id` uniquely identifies it. The example data explicitly includes IDs; relying on generated IDs would make retries impossible to recognize.
- Duplicate protection lives in the backend storage/service boundary, immediately before persistence, never only in the React UI.
- On a second request with the same ID and identical normalized payload, return the previously stored trip (`200`) without appending to `trips.json`; the daily counts and totals therefore remain unchanged.
- On same ID with a different payload, return `409` rather than silently accepting a different financial record or overwriting it.
- Test the behavior through the public create/read behavior: create once, retry, retrieve the selected day, and assert one matching trip and unchanged summary. Also test same-ID/different-payload conflict.

## 9. Test strategy

Use a runnable backend test suite without adding a test framework unless the implementation phase demonstrates a real need. The Python standard-library `unittest` runner is sufficient for this small application; isolate the JSON storage path in each test so fixtures never mutate production data.

Minimum tests:

1. Summary with mixed cash/card trips: exact count, revenue, commission, net, cash, and card totals.
2. Empty selected day: zero count and zero totals.
3. First create then identical retry: only one persisted trip and unchanged returned summary/list.
4. Same ID with different content: conflict and no overwrite.
5. Reject amount equal to zero and below zero.
6. Reject equal or reversed start/end timestamps.

Add only meaningful contract coverage: selected-day filtering using `start`, valid `cash`/`card` payment, and malformed timestamp/date handling. Do not test React internals or storage implementation details.

## 10. Implementation phases

### Phase 1 — Remove Driver Pulse scope and simplify — completed

Remove the exact unrelated files/directories and dependencies above. Preserve the Vite/FastAPI/Docker baseline, then ensure it still has a minimal working skeleton. This is a reviewable cleanup commit.

Completed on 2026-10-06. The legacy ML, prediction, stress, map, auth, goals, CSV, Streamlit, analytics, legacy deployment, and pseudo-test artifacts were removed. The backend now has only a health endpoint and the frontend is a temporary shell. The two Python dependency manifests were consolidated into the root `requirements.txt` because the remaining backend has one dependency set; no ARQA domain, storage, API, calculation, idempotency, or test behavior was added.

### Phase 2 — Establish ARQA domain, JSON storage, and calculations — completed

Add the prescribed JSON data file, schemas, deterministic storage helpers, and pure daily-summary service. Add summary unit tests before exposing the full UI.

Completed on 2026-10-06. The read-only `GET /api/trips?date=YYYY-MM-DD` endpoint reads `backend/data/trips.json`, filters by the calendar date in the offset-aware `start` timestamp, and returns the required daily summary. The JSON sample is the two official example trips. Trip creation and idempotency are intentionally not implemented.

### Phase 3 — Implement trip creation, validation, and idempotency — completed

Implement the small create/list API contract. Add validation and duplicate/conflict tests using isolated file storage.

Completed on 2026-10-06. `POST /api/trips` validates the canonical trip model and writes through the existing JSON storage. A new ID returns `201`; an exact retry with the same ID returns the existing trip with `200`; the same ID with different normalized fields returns `409` without overwriting the stored record. API-level tests use temporary JSON storage and do not modify the sample data.

### Phase 4 — Build the ARQA web client

Implement one responsive, accessible shift-diary page: selected date control, daily summary, trip list, and creation form. Use the API module and handle loading, empty, success, and error states. No unrelated dashboard or product features.

### Phase 5 — Integrate and verify locally

Run backend tests, frontend build, and Docker Compose configuration/build or start checks appropriate to the final Docker files. Manually verify create, retry, date switching, and summary refresh against the API.

### Phase 6 — README and submission preparation

Write the ARQA-specific README with prerequisites, local/Docker commands, API behavior, what is completed, and the concise AI-use/correction note. Add optional screenshots/demo only if they actually exist. Verify the public repository state before submission.

Each phase must leave the repository buildable and independently reviewable; commit them as logical units rather than one large change.

## 11. Risks and ambiguities

- The assignment says “data: a JSON file” but does not explicitly say whether newly added trips must survive a server restart. The plan uses that same JSON file for additions because it is the smallest durable implementation; a database is not justified.
- The assignment example includes `id`, but the create request contract and duplicate response status are not prescribed. Requiring a client-supplied ID and treating exact same-ID payloads as successful retries is the smallest explicit idempotency design. Same-ID/different-payload `409` is a protective implementation choice.
- It does not define which timestamp determines a day when a trip crosses midnight. The proposed consistent rule is the date of `start`; document it in the README unless ARQA clarifies otherwise.
- It does not specify allowed commission values, currency precision, rounding, sorting order, or timezone display behavior. Preserve supplied numeric values, avoid additional formulas, and sort/display explicitly only if needed for comprehensible UI.
- Monetary values are represented as integers because the supplied assignment data uses integer tenge and gives no fractional or rounding rules. Summary values are exact integer sums; no Money abstraction or commission percentage is introduced.
- The current remote deployment and README expose legacy Driver Pulse material, including demo credentials. They are outside this planning task; Phase 1/6 must remove obsolete claims and ensure no credentials or secrets remain in the final submission documentation.
