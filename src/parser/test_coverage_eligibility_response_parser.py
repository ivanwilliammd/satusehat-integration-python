"""CoverageEligibilityResponseParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.coverage_eligibility_response_parser import CoverageEligibilityResponseParser

DATA = Path(__file__).parent / "testdata" / "CoverageEligibilityResponse.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "CoverageEligibilityResponse"

    parser = CoverageEligibilityResponseParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_purpose() == data["purpose"]
    assert parser.get_patient() == data["patient"]
    assert parser.get_created() == data["created"]
    assert parser.get_requestor() == data["requestor"]
    assert parser.get_request() == data["request"]
    assert parser.get_outcome() == data["outcome"]
    assert parser.get_disposition() == data["disposition"]
    assert parser.get_insurer() == data["insurer"]
    assert parser.get_insurance() == data["insurance"]
    assert parser.get_extension() == data["extension"]
