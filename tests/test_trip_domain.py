import tempfile
import unittest
from datetime import date
from pathlib import Path

from backend.storage import TripStorage, TripStorageError
from backend.trips import Trip, calculate_daily_summary


def make_trip(**overrides: object) -> Trip:
    values = {
        "id": "t1",
        "start": "2026-10-01T08:10:00+05:00",
        "end": "2026-10-01T08:32:00+05:00",
        "amount": 2400,
        "payment": "card",
        "commission": 360,
    }
    values.update(overrides)
    return Trip.model_validate(values)


class DailySummaryTests(unittest.TestCase):
    def test_calculates_summary_for_mixed_payments(self) -> None:
        trips = [
            make_trip(),
            make_trip(
                id="t2",
                start="2026-10-01T09:05:00+05:00",
                end="2026-10-01T09:20:00+05:00",
                amount=1500,
                payment="cash",
                commission=225,
            ),
            make_trip(
                id="t3",
                start="2026-10-01T10:00:00+05:00",
                end="2026-10-01T10:25:00+05:00",
                amount=800,
                payment="card",
                commission=120,
            ),
        ]

        summary = calculate_daily_summary(trips)

        self.assertEqual(summary.trip_count, 3)
        self.assertEqual(summary.revenue, 4700)
        self.assertEqual(summary.commission, 705)
        self.assertEqual(summary.net_amount, 3995)
        self.assertEqual(summary.cash_amount, 1500)
        self.assertEqual(summary.card_amount, 3200)

    def test_calculates_zero_summary_for_no_trips(self) -> None:
        self.assertEqual(
            calculate_daily_summary([]).model_dump(),
            {
                "trip_count": 0,
                "revenue": 0,
                "commission": 0,
                "net_amount": 0,
                "cash_amount": 0,
                "card_amount": 0,
            },
        )


class TripStorageTests(unittest.TestCase):
    def test_filters_by_start_timestamp_date(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            storage = TripStorage(Path(directory) / "trips.json")
            storage.write_trips(
                [
                    make_trip(),
                    make_trip(
                        id="t2",
                        start="2026-10-02T00:05:00+05:00",
                        end="2026-10-02T00:20:00+05:00",
                    ),
                ]
            )

            trips = storage.trips_for_day(date(2026, 10, 1))

        self.assertEqual([trip.id for trip in trips], ["t1"])

    def test_missing_file_is_an_empty_data_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            storage = TripStorage(Path(directory) / "missing.json")

            self.assertEqual(storage.read_trips(), [])

    def test_empty_json_array_is_an_empty_data_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trips.json"
            path.write_text("[]", encoding="utf-8")
            storage = TripStorage(path)

            self.assertEqual(storage.read_trips(), [])

    def test_malformed_json_is_not_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trips.json"
            path.write_text("not json", encoding="utf-8")
            storage = TripStorage(path)

            with self.assertRaises(TripStorageError):
                storage.read_trips()

            self.assertEqual(path.read_text(encoding="utf-8"), "not json")
