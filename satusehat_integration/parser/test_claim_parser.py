"""ClaimParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.claim_parser import ClaimParser

DATA = Path(__file__).parent / "testdata" / "Claim.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "Claim"

    parser = ClaimParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_type() == data["type"]
    assert parser.get_use() == data["use"]
    assert parser.get_patient() == data["patient"]
    assert parser.get_billable_period() == data["billablePeriod"]
    assert parser.get_created() == data["created"]
    assert parser.get_enterer() == data["enterer"]
    assert parser.get_insurer() == data["insurer"]
    assert parser.get_provider() == data["provider"]
    assert parser.get_priority() == data["priority"]
    assert parser.get_payee() == data["payee"]
    assert parser.get_facility() == data["facility"]
    assert parser.get_supporting_info() == data["supportingInfo"]
    assert parser.get_diagnosis() == data["diagnosis"]
    assert parser.get_procedure() == data["procedure"]
    assert parser.get_insurance() == data["insurance"]
    assert parser.get_total() == data["total"]
    assert parser.get_extension() == data["extension"]
