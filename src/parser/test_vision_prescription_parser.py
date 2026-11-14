"""VisionPrescriptionParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.vision_prescription_parser import VisionPrescriptionParser

DATA = Path(__file__).parent / "testdata" / "VisionPrescription.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "VisionPrescription"

    parser = VisionPrescriptionParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_status() == data["status"]
    assert parser.get_created() == data["created"]
    assert parser.get_patient() == data["patient"]
    assert parser.get_encounter() == data["encounter"]
    assert parser.get_date_written() == data["dateWritten"]
    assert parser.get_prescriber() == data["prescriber"]
    assert parser.get_lens_specification() == data["lensSpecification"]
