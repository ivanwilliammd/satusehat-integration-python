"""EpisodeOfCareParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.episode_of_care_parser import EpisodeOfCareParser

DATA = Path(__file__).parent / "testdata" / "EpisodeOfCare.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "EpisodeOfCare"

    parser = EpisodeOfCareParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_id() == data["id"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_status_history() == data["statusHistory"]
    assert parser.get_type() == data["type"]
    assert parser.get_diagnosis() == data["diagnosis"]
    assert parser.get_patient() == data["patient"]
    assert parser.get_managing_organization() == data["managingOrganization"]
    assert parser.get_period() == data["period"]
    assert parser.get_care_manager() == data["careManager"]
