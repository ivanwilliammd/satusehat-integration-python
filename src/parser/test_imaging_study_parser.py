"""ImagingStudyParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.imaging_study_parser import ImagingStudyParser

DATA = Path(__file__).parent / "testdata" / "ImagingStudy.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "ImagingStudy"

    parser = ImagingStudyParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_id() == data["id"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_modality() == data["modality"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_started() == data["started"]
    assert parser.get_based_on() == data["basedOn"]
    assert parser.get_number_of_series() == data["numberOfSeries"]
    assert parser.get_number_of_instances() == data["numberOfInstances"]
    assert parser.get_description() == data["description"]
    assert parser.get_series() == data["series"]
