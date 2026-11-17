"""CompositionParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.composition_parser import CompositionParser

DATA = Path(__file__).parent / "testdata" / "Composition.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "Composition"

    parser = CompositionParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_status() == data["status"]
    assert parser.get_attester() == data["attester"]
    assert parser.get_type() == data["type"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_encounter() == data["encounter"]
    assert parser.get_date() == data["date"]
    assert parser.get_author() == data["author"]
    assert parser.get_title() == data["title"]
    assert parser.get_section() == data["section"]
