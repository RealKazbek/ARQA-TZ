import json
import os
import tempfile
from datetime import date
from pathlib import Path
from typing import Sequence

from pydantic import ValidationError

from backend.trips import Trip

DEFAULT_TRIPS_PATH = Path(__file__).parent / "data" / "trips.json"


class TripStorageError(RuntimeError):
    pass


class TripConflictError(RuntimeError):
    pass


def configured_trips_path() -> Path:
    configured_path = os.getenv("TRIPS_FILE_PATH")
    return Path(configured_path) if configured_path else DEFAULT_TRIPS_PATH


def initialize_trips_file(path: Path, seed_path: Path = DEFAULT_TRIPS_PATH) -> Path:
    if path.exists():
        return path

    try:
        seed_content = seed_path.read_text(encoding="utf-8")
        seed_payload = json.loads(seed_content)
        if not isinstance(seed_payload, list):
            raise TripStorageError("Seed trip storage must contain a JSON array")
        [Trip.model_validate(item) for item in seed_payload]
    except FileNotFoundError as error:
        raise TripStorageError("Seed trip storage is missing") from error
    except json.JSONDecodeError as error:
        raise TripStorageError("Seed trip storage contains invalid JSON") from error
    except ValidationError as error:
        raise TripStorageError("Seed trip storage contains an invalid trip") from error
    except OSError as error:
        raise TripStorageError("Unable to read seed trip storage") from error

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as trips_file:
            trips_file.write(seed_content)
    except FileExistsError:
        pass
    except OSError as error:
        raise TripStorageError("Unable to initialize trip storage") from error

    return path


class TripStorage:
    def __init__(self, path: Path = DEFAULT_TRIPS_PATH) -> None:
        self.path = path

    def read_trips(self) -> list[Trip]:
        try:
            raw_data = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return []
        except OSError as error:
            raise TripStorageError(f"Unable to read trip storage: {self.path}") from error

        try:
            payload = json.loads(raw_data)
        except json.JSONDecodeError as error:
            raise TripStorageError(f"Trip storage contains invalid JSON: {self.path}") from error

        if not isinstance(payload, list):
            raise TripStorageError("Trip storage must contain a JSON array")

        try:
            return [Trip.model_validate(item) for item in payload]
        except ValidationError as error:
            raise TripStorageError("Trip storage contains an invalid trip") from error

    def trips_for_day(self, selected_date: date) -> list[Trip]:
        # A trip belongs to the calendar date expressed in its start timestamp.
        return [trip for trip in self.read_trips() if trip.start.date() == selected_date]

    def add_trip(self, trip: Trip) -> tuple[Trip, bool]:
        trips = self.read_trips()

        for existing_trip in trips:
            if existing_trip.id != trip.id:
                continue
            if existing_trip.model_dump(mode="json") == trip.model_dump(mode="json"):
                return existing_trip, False
            raise TripConflictError("Trip ID already exists with different data")

        trips.append(trip)
        self.write_trips(trips)
        return trip, True

    def write_trips(self, trips: Sequence[Trip]) -> None:
        serialized = json.dumps(
            [trip.model_dump(mode="json") for trip in trips],
            ensure_ascii=False,
            indent=2,
        )

        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_file.write(f"{serialized}\n")
                temporary_path = Path(temporary_file.name)
            os.replace(temporary_path, self.path)
        except OSError as error:
            raise TripStorageError(f"Unable to write trip storage: {self.path}") from error
