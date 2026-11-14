"""SupplyRequestParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.supply_request_parser import SupplyRequestParser

DATA = Path(__file__).parent / "testdata" / "SupplyRequest.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "SupplyRequest"

    parser = SupplyRequestParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_item_reference() == data["itemReference"]
    assert parser.get_quantity() == data["quantity"]
    assert parser.get_authored_on() == data["authoredOn"]
    assert parser.get_requester() == data["requester"]
    assert parser.get_supplier() == data["supplier"]
    assert parser.get_reason_code() == data["reasonCode"]
