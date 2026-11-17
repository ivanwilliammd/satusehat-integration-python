"""NutritionOrderParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.nutrition_order_parser import NutritionOrderParser

DATA = Path(__file__).parent / "testdata" / "NutritionOrder.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "NutritionOrder"

    parser = NutritionOrderParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_intent() == data["intent"]
    assert parser.get_patient() == data["patient"]
    assert parser.get_encounter() == data["encounter"]
    assert parser.get_date_time() == data["dateTime"]
    assert parser.get_oral_diet() == data["oralDiet"]
