"""PaymentNotice: 14 setter PHP, tiga di antaranya menulis elemen yang tidak sah R4."""
import json
from pathlib import Path

from satusehat_integration.builder.payment_notice import PaymentNoticeBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> PaymentNoticeBuilder:
    return (
        PaymentNoticeBuilder()
        .set_id("pn-1")
        .add_identifier("http://sys.id/ni", "NI-1300")
        .set_status("active")
        .set_request("Claim/clm-1")
        .set_response("ClaimResponse/cr-1")
        .set_status_date("2026-01-07")
        .set_created("2026-01-07T09:00:00+07:00")
        .set_provider("Organization/1000000001")
        .set_payee("Organization/1000000002")
        .set_payment(250000.0, "IDR")
        .set_payment_date("2026-01-07")
        .set_payment_status("http://terminology.hl7.org/CodeSystem/paymentstatus", "paid", "Dibayar")
        .set_insurer("Organization/1000000003")
        .set_payment_reconciliation("PaymentReconciliation/pr-1")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("payment_notice")


def test_quirk_payment_berisi_amount_bukan_reference():
    """R4: PaymentNotice.payment bertipe Reference; Money tinggal di `amount`."""
    payment = isi().build()["payment"]
    assert payment == {"amount": {"value": 250000.0, "currency": "IDR"}}
    assert "reference" not in payment


def test_dua_elemen_yang_tidak_ada_di_r4_tetap_ditulis():
    hasil = isi().build()
    assert "insurer" in hasil
    assert "paymentReconciliation" in hasil
    assert "amount" not in hasil


def test_tambahan_amount_menulis_money_yang_sah():
    hasil = PaymentNoticeBuilder().amount(1000.0, "IDR").build()
    assert hasil["amount"] == {"value": 1000.0, "currency": "IDR"}


def test_alias_lama_tetap_jalan():
    assert PaymentNoticeBuilder().status("active").build()["status"] == "active"
