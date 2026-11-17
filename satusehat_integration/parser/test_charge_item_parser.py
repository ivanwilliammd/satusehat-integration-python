"""ChargeItemParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.charge_item_parser import ChargeItemParser

DATA = Path(__file__).parent / "testdata" / "ChargeItem.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "ChargeItem"

    parser = ChargeItemParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_status() == data["status"]
    assert parser.get_code() == data["code"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_context() == data["context"]
    assert parser.get_occurrence_period() == data["occurrencePeriod"]
    assert parser.get_performer() == data["performer"]
    assert parser.get_quantity() == data["quantity"]
    assert parser.get_account() == data["account"]
    assert parser.get_extension() == data["extension"]
