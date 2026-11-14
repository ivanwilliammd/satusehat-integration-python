"""QuestionnaireResponseParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.questionnaire_response_parser import QuestionnaireResponseParser

DATA = Path(__file__).parent / "testdata" / "QuestionnaireResponse.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "QuestionnaireResponse"

    parser = QuestionnaireResponseParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_questionnaire() == data["questionnaire"]
    assert parser.get_status() == data["status"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_encounter() == data["encounter"]
    assert parser.get_authored() == data["authored"]
    assert parser.get_author() == data["author"]
    assert parser.get_source() == data["source"]
    assert parser.get_item() == data["item"]
