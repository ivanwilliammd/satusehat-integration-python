"""CarePlanParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.care_plan_parser import CarePlanParser

DATA = Path(__file__).parent / "testdata" / "CarePlan.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "CarePlan"

    parser = CarePlanParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_title() == data["title"]
    assert parser.get_description() == data["description"]
    assert parser.get_category() == data["category"]
    assert parser.get_status() == data["status"]
    assert parser.get_intent() == data["intent"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_encounter() == data["encounter"]
    assert parser.get_period() == data["period"]
    assert parser.get_created() == data["created"]
    assert parser.get_author() == data["author"]
    assert parser.get_activity() == data["activity"]
