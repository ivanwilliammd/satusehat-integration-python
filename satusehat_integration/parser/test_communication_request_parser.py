"""CommunicationRequestParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.communication_request_parser import CommunicationRequestParser

DATA = Path(__file__).parent / "testdata" / "CommunicationRequest.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "CommunicationRequest"

    parser = CommunicationRequestParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_status() == data["status"]
    assert parser.get_category() == data["category"]
    assert parser.get_payload() == data["payload"]
    assert parser.get_about() == data["about"]
    assert parser.get_sender() == data["sender"]
    assert parser.get_recipient() == data["recipient"]
