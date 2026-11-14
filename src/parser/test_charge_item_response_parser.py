"""ChargeItemResponseParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.charge_item_response_parser import ChargeItemResponseParser

DATA = Path(__file__).parent / "testdata" / "ChargeItemResponse.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "ChargeItemResponse"

    parser = ChargeItemResponseParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_id() == data["id"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_charge_item() == data["chargeItem"]
    assert parser.get_coverage() == data["coverage"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_encounter() == data["encounter"]
    assert parser.get_payor() == data["payor"]
    assert parser.get_quantity() == data["quantity"]
    assert parser.get_unit_price_override() == data["unitPriceOverride"]
    assert parser.get_factor_override() == data["factorOverride"]
    assert parser.get_override_reason() == data["overrideReason"]
    assert parser.get_total() == data["total"]
    assert parser.get_excess() == data["excess"]
