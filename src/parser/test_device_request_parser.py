"""DeviceRequestParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.device_request_parser import DeviceRequestParser

DATA = Path(__file__).parent / "testdata" / "DeviceRequest.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "DeviceRequest"

    parser = DeviceRequestParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_intent() == data["intent"]
    assert parser.get_priority() == data["priority"]
    assert parser.get_code_reference() == data["codeReference"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_authored_on() == data["authoredOn"]
    assert parser.get_requester() == data["requester"]
    assert parser.get_performer() == data["performer"]
    assert parser.get_reason_code() == data["reasonCode"]
