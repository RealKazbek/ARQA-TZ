from datetime import date

from fastapi import FastAPI

from backend.storage import DEFAULT_TRIPS_PATH, TripStorage
from backend.trips import DailyTrips, calculate_daily_summary

app = FastAPI(title="Driver Shift Diary API", version="0.1.0")
trip_storage = TripStorage(DEFAULT_TRIPS_PATH)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/trips", response_model=DailyTrips)
def list_trips(date: date) -> DailyTrips:
    trips = trip_storage.trips_for_day(date)
    return DailyTrips(date=date, trips=trips, summary=calculate_daily_summary(trips))
