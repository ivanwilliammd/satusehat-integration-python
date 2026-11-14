"""FamilyMemberHistoryParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.family_member_history_parser import FamilyMemberHistoryParser

DATA = Path(__file__).parent / "testdata" / "FamilyMemberHistory.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "FamilyMemberHistory"

    parser = FamilyMemberHistoryParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_status() == data["status"]
    assert parser.get_relationship() == data["relationship"]
    assert parser.get_deceased_boolean() == data["deceasedBoolean"]
    assert parser.get_patient() == data["patient"]
    assert parser.get_date() == data["date"]
    assert parser.get_condition() == data["condition"]
