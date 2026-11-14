"""MedicationRequestParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.medication_request_parser import MedicationRequestParser

DATA = Path(__file__).parent / "testdata" / "MedicationRequest.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "MedicationRequest"

    parser = MedicationRequestParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_contained() == data["contained"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_intent() == data["intent"]
    assert parser.get_category() == data["category"]
    assert parser.get_priority() == data["priority"]
    assert parser.get_medication_reference() == data["medicationReference"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_encounter() == data["encounter"]
    assert parser.get_authored_on() == data["authoredOn"]
    assert parser.get_requester() == data["requester"]
    assert parser.get_course_of_therapy_type() == data["courseOfTherapyType"]
    assert parser.get_dosage_instruction() == data["dosageInstruction"]
    assert parser.get_dispense_request() == data["dispenseRequest"]
