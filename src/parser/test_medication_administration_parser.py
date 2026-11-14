"""MedicationAdministrationParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.medication_administration_parser import MedicationAdministrationParser

DATA = Path(__file__).parent / "testdata" / "MedicationAdministration.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "MedicationAdministration"

    parser = MedicationAdministrationParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_contained() == data["contained"]
    assert parser.get_status() == data["status"]
    assert parser.get_category() == data["category"]
    assert parser.get_medication_reference() == data["medicationReference"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_context() == data["context"]
    assert parser.get_effective_period() == data["effectivePeriod"]
    assert parser.get_performer() == data["performer"]
    assert parser.get_reason_code() == data["reasonCode"]
    assert parser.get_request() == data["request"]
    assert parser.get_dosage() == data["dosage"]
