"""PaymentReconciliationParser tested against the official example payload: every accessor must return the same
element the payload holds."""
import json
from pathlib import Path

from src.parser.payment_reconciliation_parser import PaymentReconciliationParser

DATA = Path(__file__).parent / "testdata" / "PaymentReconciliation.json"


def test_matches_official_example() -> None:
    data = json.loads(DATA.read_text())
    assert data["resourceType"] == "PaymentReconciliation"

    parser = PaymentReconciliationParser(data)
    assert parser.get_raw() == data
    assert parser.get_resource_type() == data["resourceType"]
    assert parser.get_status() == data["status"]
    assert parser.get_period() == data["period"]
    assert parser.get_created() == data["created"]
    assert parser.get_payment_issuer() == data["paymentIssuer"]
    assert parser.get_requestor() == data["requestor"]
    assert parser.get_outcome() == data["outcome"]
    assert parser.get_disposition() == data["disposition"]
    assert parser.get_payment_date() == data["paymentDate"]
    assert parser.get_payment_amount() == data["paymentAmount"]
    assert parser.get_detail() == data["detail"]
    assert parser.get_process_note() == data["processNote"]
