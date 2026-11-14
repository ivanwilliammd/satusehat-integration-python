"""MedicationDispenseParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.medication_dispense_parser import MedicationDispenseParser

DATA = Path(__file__).parent / "testdata" / "MedicationDispense.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "MedicationDispense"

    parser = MedicationDispenseParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_contained() == data["contained"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_category() == data["category"]
    assert parser.get_medication_reference() == data["medicationReference"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_context() == data["context"]
    assert parser.get_performer() == data["performer"]
    assert parser.get_location() == data["location"]
    assert parser.get_authorizing_prescription() == data["authorizingPrescription"]
    assert parser.get_quantity() == data["quantity"]
    assert parser.get_days_supply() == data["daysSupply"]
    assert parser.get_when_prepared() == data["whenPrepared"]
    assert parser.get_when_handed_over() == data["whenHandedOver"]
    assert parser.get_dosage_instruction() == data["dosageInstruction"]
