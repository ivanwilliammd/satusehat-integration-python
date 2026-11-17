"""BillingStatusParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.billing_status_parser import BillingStatusParser

DATA = Path(__file__).parent / "testdata" / "BillingStatus.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "BillingStatus"

    parser = BillingStatusParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_id() == data["id"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_insurer() == data["insurer"]
    assert parser.get_recipient() == data["recipient"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_request() == data["request"]
