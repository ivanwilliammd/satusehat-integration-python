"""ConditionParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.condition_parser import ConditionParser

DATA = Path(__file__).parent / "testdata" / "Condition.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "Condition"

    parser = ConditionParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_clinical_status() == data["clinicalStatus"]
    assert parser.get_verification_status() == data["verificationStatus"]
    assert parser.get_category() == data["category"]
    assert parser.get_code() == data["code"]
    assert parser.get_stage() == data["stage"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_encounter() == data["encounter"]
    assert parser.get_recorded_date() == data["recordedDate"]
