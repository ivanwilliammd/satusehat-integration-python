"""CoverageEligibilityRequestParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.coverage_eligibility_request_parser import CoverageEligibilityRequestParser

DATA = Path(__file__).parent / "testdata" / "CoverageEligibilityRequest.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "CoverageEligibilityRequest"

    parser = CoverageEligibilityRequestParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_priority() == data["priority"]
    assert parser.get_purpose() == data["purpose"]
    assert parser.get_patient() == data["patient"]
    assert parser.get_serviced_date() == data["servicedDate"]
    assert parser.get_created() == data["created"]
    assert parser.get_enterer() == data["enterer"]
    assert parser.get_provider() == data["provider"]
    assert parser.get_insurer() == data["insurer"]
    assert parser.get_facility() == data["facility"]
    assert parser.get_insurance() == data["insurance"]
    assert parser.get_supporting_info() == data["supportingInfo"]
    assert parser.get_contained() == data["contained"]
