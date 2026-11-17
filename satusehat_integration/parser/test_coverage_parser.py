"""CoverageParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.coverage_parser import CoverageParser

DATA = Path(__file__).parent / "testdata" / "Coverage.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "Coverage"

    parser = CoverageParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_type() == data["type"]
    assert parser.get_subscriber_id() == data["subscriberId"]
    assert parser.get_beneficiary() == data["beneficiary"]
    assert parser.get_payor() == data["payor"]
    assert parser.get_class() == data["class"]
    assert parser.get_extension() == data["extension"]
