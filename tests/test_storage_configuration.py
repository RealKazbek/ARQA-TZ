import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.storage import (
    DEFAULT_TRIPS_PATH,
    TripStorage,
    TripStorageError,
    configured_trips_path,
    initialize_trips_file,
)


class TripStorageConfigurationTests(unittest.TestCase):
    def test_configured_trips_file_path_is_used(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "persistent" / "trips.json"

            with patch.dict(os.environ, {"TRIPS_FILE_PATH": str(path)}):
                self.assertEqual(configured_trips_path(), path)

            initialize_trips_file(path)
            self.assertEqual(TripStorage(path).read_trips(), TripStorage(DEFAULT_TRIPS_PATH).read_trips())

    def test_missing_persistent_file_is_initialized_from_seed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data" / "trips.json"

            initialize_trips_file(path)

            self.assertEqual(path.read_text(encoding="utf-8"), DEFAULT_TRIPS_PATH.read_text(encoding="utf-8"))

    def test_existing_persistent_file_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trips.json"
            existing_data = json.dumps(
                [
                    {
                        "id": "persisted-trip",
                        "start": "2026-10-05T08:00:00+05:00",
                        "end": "2026-10-05T08:15:00+05:00",
                        "amount": 1000,
                        "payment": "card",
                        "commission": 150,
                    }
                ]
            )
            path.write_text(existing_data, encoding="utf-8")

            initialize_trips_file(path)

            self.assertEqual(path.read_text(encoding="utf-8"), existing_data)

    def test_malformed_persistent_file_is_not_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trips.json"
            path.write_text("not json", encoding="utf-8")

            initialize_trips_file(path)

            self.assertEqual(path.read_text(encoding="utf-8"), "not json")
            with self.assertRaises(TripStorageError):
                TripStorage(path).read_trips()
