"""ClaimResponseParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.claim_response_parser import ClaimResponseParser

DATA = Path(__file__).parent / "testdata" / "ClaimResponse.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "ClaimResponse"

    parser = ClaimResponseParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_status() == data["status"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_type() == data["type"]
    assert parser.get_use() == data["use"]
    assert parser.get_patient() == data["patient"]
    assert parser.get_created() == data["created"]
    assert parser.get_insurer() == data["insurer"]
    assert parser.get_requestor() == data["requestor"]
    assert parser.get_request() == data["request"]
    assert parser.get_outcome() == data["outcome"]
    assert parser.get_payee_type() == data["payeeType"]
    assert parser.get_adjudication() == data["adjudication"]
    assert parser.get_item() == data["item"]
    assert parser.get_total() == data["total"]
    assert parser.get_payment() == data["payment"]
