"""DeviceUseStatementParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.device_use_statement_parser import DeviceUseStatementParser

DATA = Path(__file__).parent / "testdata" / "DeviceUseStatement.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "DeviceUseStatement"

    parser = DeviceUseStatementParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_device() == data["device"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_timing_period() == data["timingPeriod"]
    assert parser.get_recorded_on() == data["recordedOn"]
    assert parser.get_source() == data["source"]
    assert parser.get_reason_code() == data["reasonCode"]
    assert parser.get_note() == data["note"]
