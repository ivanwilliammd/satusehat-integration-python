"""AccountParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.account_parser import AccountParser

DATA = Path(__file__).parent / "testdata" / "Account.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "Account"

    parser = AccountParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_status() == data["status"]
    assert parser.get_type() == data["type"]
    assert parser.get_name() == data["name"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_service_period() == data["servicePeriod"]
    assert parser.get_owner() == data["owner"]
    assert parser.get_guarantor() == data["guarantor"]
    assert parser.get_description() == data["description"]
