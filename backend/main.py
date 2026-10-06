import os
from datetime import date

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from backend.storage import TripConflictError, TripStorage, configured_trips_path, initialize_trips_file
from backend.trips import DailyTrips, Trip, calculate_daily_summary

app = FastAPI(
    title="Driver Shift Diary API",
    description=(
        "ARQA technical assignment API for viewing a driver's daily trips and summary, "
        "and adding retry-safe trips backed by JSON storage."
    ),
    version="0.1.0",
)
frontend_origin = os.getenv("FRONTEND_ORIGIN")
if frontend_origin:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_origin],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

trip_storage = TripStorage(initialize_trips_file(configured_trips_path()))


@app.get("/api/health", summary="Check API health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get(
    "/api/trips",
    response_model=DailyTrips,
    summary="Get trips and summary for one day",
    description="Trips are selected by the calendar date in each trip's `start` timestamp.",
)
def list_trips(date: date) -> DailyTrips:
    trips = trip_storage.trips_for_day(date)
    return DailyTrips(date=date, trips=trips, summary=calculate_daily_summary(trips))


@app.post(
    "/api/trips",
    response_model=Trip,
    status_code=status.HTTP_201_CREATED,
    summary="Create an idempotent trip",
    description=(
        "A new trip ID is stored and returns `201`. Retrying the identical payload returns "
        "the existing trip with `200` and does not create a duplicate. Reusing an ID with "
        "different data returns `409`."
    ),
    responses={
        status.HTTP_200_OK: {"description": "Identical retry; the existing trip is returned."},
        status.HTTP_409_CONFLICT: {"description": "The trip ID already exists with different data."},
    },
)
def create_trip(trip: Trip, response: Response) -> Trip:
    try:
        stored_trip, created = trip_storage.add_trip(trip)
    except TripConflictError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from None

    if not created:
        response.status_code = status.HTTP_200_OK
    return stored_trip
