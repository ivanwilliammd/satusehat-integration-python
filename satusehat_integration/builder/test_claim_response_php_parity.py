"""ClaimResponse: 24 setter PHP, dibandingkan dengan golden yang dibuat dari PHP."""
import json
from pathlib import Path

from satusehat_integration.builder.claim_response import ClaimResponseBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"
ADJ = "http://terminology.hl7.org/CodeSystem/adjudication"
KFA = "http://sys-ids.kemkes.go.id/kfa"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> ClaimResponseBuilder:
    return (
        ClaimResponseBuilder()
        .set_id("cr-1")
        .add_identifier("http://sys.id/ni", "NI-600")
        .set_status("active")
        .set_type("http://terminology.hl7.org/CodeSystem/claim-type", "institutional", "Institusi")
        .set_sub_type("http://terminology.hl7.org/CodeSystem/ex-claimsubtype", "subrogation", "Subrogasi")
        .set_use("claim")
        .set_patient("Patient/1000000001")
        .set_created("2026-01-06T10:00:00+07:00")
        .set_insurer("Organization/1000000003")
        .set_requestor("Organization/1000000001")
        .set_request("Claim/clm-1")
        .set_outcome("complete")
        .set_disposition("Setuju sebagian")
        .set_pre_auth_ref("PA-77")
        .set_pre_auth_period("2026-01-05", "2026-02-05")
        .set_payee_type("http://terminology.hl7.org/CodeSystem/payeetype", "provider", "Provider")
        .add_item(1)
        .add_item(2, 1, 1)
        .add_item_adjudication(1, ADJ, "eligible", 300000.0)
        .add_item_adjudication(
            1, ADJ, "copay", 50000.0, "http://terminology.hl7.org/CodeSystem/adjudication-reason", "ar002"
        )
        .add_add_item(1, KFA, "93000515", "Amoksisilin")
        .add_add_item_adjudication(1, ADJ, "eligible", 15000.0)
        .add_add_item(2, KFA, "93000516", "Parasetamol")
        .add_add_item_adjudication(2, ADJ, "eligible", 5000.0)
        .add_error(2, "http://terminology.hl7.org/CodeSystem/adjudication-error", "a001", "Kode tidak dikenal")
        .add_coverage(1, "Coverage/cov-1", True)
        .add_coverage(2, "Coverage/cov-2", False, "http://terminology.hl7.org/CodeSystem/coverage-priority", "2")
        .set_total(300000.0, ADJ, "eligible")
        .set_total(50000.0, ADJ, "copay")
        .set_payment(250000.0, "http://terminology.hl7.org/CodeSystem/payment-type", "complete", "2026-01-07", "Payment/pay-1")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("claim_response")


def test_adjudikasi_menumpuk_ke_item_bukan_ke_item_adjudication():
    item = isi().build()["item"]
    assert len(item) == 4
    assert item[2]["category"]["coding"][0]["code"] == "eligible"


def test_adjudikasi_add_item_menempel_ke_add_item_terakhir():
    add_item = isi().build()["addItem"]
    assert len(add_item[0]["adjudication"]) == 1
    assert add_item[1]["adjudication"][0]["value"] == 5000.0


def test_payment_menulis_type_date_amount_dan_reference():
    payment = isi().build()["payment"]
    assert payment["amount"] == {"value": 250000.0}
    assert payment["reference"] == "Payment/pay-1"


def test_set_total_menumpuk():
    assert len(isi().build()["total"]) == 2
