import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from backend import main
from backend.storage import TripStorage


def trip_payload(**overrides: object) -> dict[str, object]:
    payload = {
        "id": "new-trip-1",
        "start": "2026-10-01T10:00:00+05:00",
        "end": "2026-10-01T10:20:00+05:00",
        "amount": 1800,
        "payment": "cash",
        "commission": 270,
    }
    payload.update(overrides)
    return payload


class TripApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.original_storage = main.trip_storage
        main.trip_storage = TripStorage(Path(self.temporary_directory.name) / "trips.json")
        self.client = TestClient(main.app)

    def tearDown(self) -> None:
        main.trip_storage = self.original_storage
        self.temporary_directory.cleanup()

    def test_creates_a_valid_trip(self) -> None:
        payload = trip_payload()

        response = self.client.post("/api/trips", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), payload)
        self.assertEqual(
            [trip.model_dump(mode="json") for trip in main.trip_storage.read_trips()],
            [payload],
        )

    def test_retries_an_identical_trip_without_creating_a_duplicate(self) -> None:
        payload = trip_payload()

        first_response = self.client.post("/api/trips", json=payload)
        retry_response = self.client.post("/api/trips", json=payload)

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(retry_response.status_code, 200)
        self.assertEqual(retry_response.json(), payload)
        self.assertEqual(len(main.trip_storage.read_trips()), 1)

    def test_rejects_zero_amount_without_writing(self) -> None:
        response = self.client.post("/api/trips", json=trip_payload(amount=0))

        self.assertEqual(response.status_code, 422)
        self.assertEqual(main.trip_storage.read_trips(), [])

    def test_rejects_negative_amount_without_writing(self) -> None:
        response = self.client.post("/api/trips", json=trip_payload(amount=-1))

        self.assertEqual(response.status_code, 422)
        self.assertEqual(main.trip_storage.read_trips(), [])

    def test_rejects_equal_start_and_end_without_writing(self) -> None:
        response = self.client.post(
            "/api/trips",
            json=trip_payload(end="2026-10-01T10:00:00+05:00"),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(main.trip_storage.read_trips(), [])

    def test_rejects_end_before_start_without_writing(self) -> None:
        response = self.client.post(
            "/api/trips",
            json=trip_payload(end="2026-10-01T09:59:00+05:00"),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(main.trip_storage.read_trips(), [])

    def test_creates_multiple_trips_with_distinct_ids(self) -> None:
        first_response = self.client.post("/api/trips", json=trip_payload())
        second_response = self.client.post(
            "/api/trips",
            json=trip_payload(
                id="new-trip-2",
                start="2026-10-01T11:00:00+05:00",
                end="2026-10-01T11:15:00+05:00",
                amount=900,
                payment="card",
                commission=135,
            ),
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 201)
        self.assertEqual([trip.id for trip in main.trip_storage.read_trips()], ["new-trip-1", "new-trip-2"])

    def test_rejects_conflicting_trip_id_without_overwriting(self) -> None:
        original_payload = trip_payload()
        self.client.post("/api/trips", json=original_payload)

        response = self.client.post("/api/trips", json=trip_payload(amount=1900))

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {"detail": "Trip ID already exists with different data"})
        self.assertEqual(
            [trip.model_dump(mode="json") for trip in main.trip_storage.read_trips()],
            [original_payload],
        )

    def test_created_trip_is_included_in_the_daily_read_response(self) -> None:
        payload = trip_payload()
        self.client.post("/api/trips", json=payload)

        response = self.client.get("/api/trips?date=2026-10-01")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["trips"], [payload])
        self.assertEqual(
            response.json()["summary"],
            {
                "trip_count": 1,
                "revenue": 1800,
                "commission": 270,
                "net_amount": 1530,
                "cash_amount": 1800,
                "card_amount": 0,
            },
        )
