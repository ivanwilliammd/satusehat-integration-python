"""SupplyDeliveryParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.supply_delivery_parser import SupplyDeliveryParser

DATA = Path(__file__).parent / "testdata" / "SupplyDelivery.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "SupplyDelivery"

    parser = SupplyDeliveryParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_based_on() == data["basedOn"]
    assert parser.get_status() == data["status"]
    assert parser.get_patient() == data["patient"]
    assert parser.get_supplied_item() == data["suppliedItem"]
    assert parser.get_occurrence_date_time() == data["occurrenceDateTime"]
    assert parser.get_supplier() == data["supplier"]
    assert parser.get_destination() == data["destination"]
    assert parser.get_receiver() == data["receiver"]
