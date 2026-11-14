"""ClinicalImpressionParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.clinical_impression_parser import ClinicalImpressionParser

DATA = Path(__file__).parent / "testdata" / "ClinicalImpression.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "ClinicalImpression"

    parser = ClinicalImpressionParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_code() == data["code"]
    assert parser.get_description() == data["description"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_encounter() == data["encounter"]
    assert parser.get_effective_date_time() == data["effectiveDateTime"]
    assert parser.get_date() == data["date"]
    assert parser.get_assessor() == data["assessor"]
    assert parser.get_problem() == data["problem"]
    assert parser.get_investigation() == data["investigation"]
    assert parser.get_summary() == data["summary"]
    assert parser.get_finding() == data["finding"]
    assert parser.get_prognosis_codeable_concept() == data["prognosisCodeableConcept"]
