"""PaymentReconciliation: 20 setter PHP yang sebelumnya tidak ada di Python."""
import json
from pathlib import Path

from src.builder.payment_reconciliation import PaymentReconciliationBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> PaymentReconciliationBuilder:
    return (
        PaymentReconciliationBuilder()
        .set_id("pr-1")
        .add_identifier("http://sys.id/ni", "NI-900")
        .set_status("active")
        .set_type("http://terminology.hl7.org/CodeSystem/payment-type", "payment", "Pembayaran")
        .set_created("2026-01-08T09:00:00+07:00")
        .set_period("2026-01-01", "2026-01-31")
        .set_request("Claim/clm-1")
        .set_request_provider("Organization/1000000001")
        .set_outcome("http://terminology.hl7.org/CodeSystem/remittance-advice", "complete", "Selesai")
        .set_disposition("Setuju sebagian")
        .set_insurer("Organization/1000000003")
        .set_request_match_date("2026-01-07")
        .set_outcome_code("http://terminology.hl7.org/CodeSystem/adjudication", "eligible", "Eligible")
        .add_requestor("Practitioner/1000000002", "dr. Ani")
        .add_process_note("Diverifikasi manual")
        .set_payment_date("2026-01-09")
        .set_payment_amount(250000.0, "IDR")
        .set_payment_identifier("http://sys.id/payment", "PAY-1")
        .add_detail("http://terminology.hl7.org/CodeSystem/adjudication", "copay", 50000.0, "Claim/clm-1")
        .add_detail("http://terminology.hl7.org/CodeSystem/adjudication", "eligible", 300000.0)
        .set_total_amount(250000.0, "IDR")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("payment_reconciliation")


def test_period_end_tidak_lagi_menulis_elemen_periodEnd():
    hasil = isi().build()
    assert hasil["period"] == {"start": "2026-01-01", "end": "2026-01-31"}
    assert "periodEnd" not in hasil


def test_outcome_bertipe_codeable_concept():
    hasil = isi().build()
    assert hasil["outcome"]["coding"][0]["code"] == "complete"


def test_detail_menumpuk_dan_amount_opsional():
    hasil = isi().build()
    assert len(hasil["detail"]) == 2
    assert hasil["detail"][1]["amount"] == {"value": 300000.0}


def test_payment_amount_dan_total_amount_bersarang():
    hasil = isi().build()
    assert hasil["paymentAmount"] == {"value": 250000.0, "currency": "IDR"}
    assert hasil["totalAmount"] == {"value": 250000.0, "currency": "IDR"}


def test_alias_lama_masih_jalan():
    b = PaymentReconciliationBuilder().period_start("2026-01-01").period_end("2026-01-31")
    assert b.build()["period"] == {"start": "2026-01-01", "end": "2026-01-31"}
