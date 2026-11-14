"""AllergyIntoleranceParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.allergy_intolerance_parser import AllergyIntoleranceParser

DATA = Path(__file__).parent / "testdata" / "AllergyIntolerance.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "AllergyIntolerance"

    parser = AllergyIntoleranceParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_clinical_status() == data["clinicalStatus"]
    assert parser.get_verification_status() == data["verificationStatus"]
    assert parser.get_category() == data["category"]
    assert parser.get_code() == data["code"]
    assert parser.get_patient() == data["patient"]
    assert parser.get_encounter() == data["encounter"]
    assert parser.get_recorded_date() == data["recordedDate"]
    assert parser.get_recorder() == data["recorder"]
