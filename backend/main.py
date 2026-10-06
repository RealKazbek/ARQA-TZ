from datetime import date

from fastapi import FastAPI, HTTPException, Response, status

from backend.storage import DEFAULT_TRIPS_PATH, TripConflictError, TripStorage
from backend.trips import DailyTrips, Trip, calculate_daily_summary

app = FastAPI(title="Driver Shift Diary API", version="0.1.0")
trip_storage = TripStorage(DEFAULT_TRIPS_PATH)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/trips", response_model=DailyTrips)
def list_trips(date: date) -> DailyTrips:
    trips = trip_storage.trips_for_day(date)
    return DailyTrips(date=date, trips=trips, summary=calculate_daily_summary(trips))


@app.post("/api/trips", response_model=Trip, status_code=status.HTTP_201_CREATED)
def create_trip(trip: Trip, response: Response) -> Trip:
    try:
        stored_trip, created = trip_storage.add_trip(trip)
    except TripConflictError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from None

    if not created:
        response.status_code = status.HTTP_200_OK
    return stored_trip
