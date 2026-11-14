"""MedicationParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.medication_parser import MedicationParser

DATA = Path(__file__).parent / "testdata" / "Medication.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "Medication"

    parser = MedicationParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_meta() == data["meta"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_code() == data["code"]
    assert parser.get_status() == data["status"]
    assert parser.get_manufacturer() == data["manufacturer"]
    assert parser.get_form() == data["form"]
    assert parser.get_ingredient() == data["ingredient"]
    assert parser.get_batch() == data["batch"]
    assert parser.get_extension() == data["extension"]
