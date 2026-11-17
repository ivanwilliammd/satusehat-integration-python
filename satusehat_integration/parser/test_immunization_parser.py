"""ImmunizationParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.immunization_parser import ImmunizationParser

DATA = Path(__file__).parent / "testdata" / "Immunization.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "Immunization"

    parser = ImmunizationParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_status() == data["status"]
    assert parser.get_vaccine_code() == data["vaccineCode"]
    assert parser.get_patient() == data["patient"]
    assert parser.get_encounter() == data["encounter"]
    assert parser.get_occurrence_date_time() == data["occurrenceDateTime"]
    assert parser.get_recorded() == data["recorded"]
    assert parser.get_reaction() == data["reaction"]
    assert parser.get_primary_source() == data["primarySource"]
    assert parser.get_location() == data["location"]
    assert parser.get_lot_number() == data["lotNumber"]
    assert parser.get_expiration_date() == data["expirationDate"]
    assert parser.get_route() == data["route"]
    assert parser.get_dose_quantity() == data["doseQuantity"]
    assert parser.get_performer() == data["performer"]
    assert parser.get_reason_code() == data["reasonCode"]
    assert parser.get_protocol_applied() == data["protocolApplied"]
