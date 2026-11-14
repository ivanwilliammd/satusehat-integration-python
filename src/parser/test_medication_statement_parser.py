"""MedicationStatementParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.medication_statement_parser import MedicationStatementParser

DATA = Path(__file__).parent / "testdata" / "MedicationStatement.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "MedicationStatement"

    parser = MedicationStatementParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_contained() == data["contained"]
    assert parser.get_status() == data["status"]
    assert parser.get_category() == data["category"]
    assert parser.get_medication_reference() == data["medicationReference"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_dosage() == data["dosage"]
    assert parser.get_effective_date_time() == data["effectiveDateTime"]
    assert parser.get_date_asserted() == data["dateAsserted"]
    assert parser.get_information_source() == data["informationSource"]
    assert parser.get_context() == data["context"]
