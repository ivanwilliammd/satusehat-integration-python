"""PaymentNoticeParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from satusehat_integration.parser.payment_notice_parser import PaymentNoticeParser

DATA = Path(__file__).parent / "testdata" / "PaymentNotice.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "PaymentNotice"

    parser = PaymentNoticeParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_status() == data["status"]
    assert parser.get_request() == data["request"]
    assert parser.get_response() == data["response"]
    assert parser.get_created() == data["created"]
    assert parser.get_payment_date() == data["paymentDate"]
    assert parser.get_provider() == data["provider"]
    assert parser.get_payee() == data["payee"]
    assert parser.get_recipient() == data["recipient"]
    assert parser.get_amount() == data["amount"]
    assert parser.get_payment() == data["payment"]
    assert parser.get_payment_status() == data["paymentStatus"]
