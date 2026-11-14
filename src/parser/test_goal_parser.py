"""GoalParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.goal_parser import GoalParser

DATA = Path(__file__).parent / "testdata" / "Goal.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "Goal"

    parser = GoalParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_id() == data["id"]
    assert parser.get_lifecycle_status() == data["lifecycleStatus"]
    assert parser.get_achievement_status() == data["achievementStatus"]
    assert parser.get_category() == data["category"]
    assert parser.get_description() == data["description"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_target() == data["target"]
    assert parser.get_status_date() == data["statusDate"]
    assert parser.get_expressed_by() == data["expressedBy"]
    assert parser.get_addresses() == data["addresses"]
    assert parser.get_outcome_code() == data["outcomeCode"]
