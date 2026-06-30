"""Seed data loader for the Vehicles bounded context.

Reads the static fixture file and returns raw dicts.
No domain or application logic lives here.
"""

import json
from pathlib import Path

_FIXTURE_PATH = Path(__file__).parent / "car_fixtures.json"


def load_car_fixtures() -> list[dict]:
    """Return the list of car fixture dicts from the JSON file.

    Returns:
        list[dict]: Raw fixture records ready to be consumed by the
        application seed handler.

    Raises:
        FileNotFoundError: If the fixture file is missing.
        json.JSONDecodeError: If the fixture file contains invalid JSON.
    """
    with _FIXTURE_PATH.open(encoding="utf-8") as f:
        return json.load(f)