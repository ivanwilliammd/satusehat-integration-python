"""InvoiceParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.invoice_parser import InvoiceParser

DATA = Path(__file__).parent / "testdata" / "Invoice.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "Invoice"

    parser = InvoiceParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_status() == data["status"]
    assert parser.get_subject() == data["subject"]
    assert parser.get_date() == data["date"]
    assert parser.get_issuer() == data["issuer"]
    assert parser.get_account() == data["account"]
    assert parser.get_line_item() == data["lineItem"]
    assert parser.get_total_net() == data["totalNet"]
