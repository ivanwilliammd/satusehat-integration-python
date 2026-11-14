"""DeviceDispenseParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.device_dispense_parser import DeviceDispenseParser

DATA = Path(__file__).parent / "testdata" / "DeviceDispense.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "DeviceDispense"

    parser = DeviceDispenseParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_identifier() == data["identifier"]
    assert parser.get_status() == data["status"]
    assert parser.get_based_on() == data["basedOn"]
    assert parser.get_device() == data["device"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_receiver() == data["receiver"]
    assert parser.get_performer() == data["performer"]
    assert parser.get_when_prepared() == data["whenPrepared"]
    assert parser.get_when_handed_over() == data["whenHandedOver"]
    assert parser.get_destination() == data["destination"]
    assert parser.get_note() == data["note"]
