"""Invoice: 20 setter PHP, dengan priceComponent bersarang per lineItem."""
import json
from pathlib import Path

from src.builder.invoice import InvoiceBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"
KFA = "http://sys-ids.kemkes.go.id/kfa"
PROC = "http://terminology.kemkes.go.id/CodeSystem/procedure"
PART = "http://terminology.hl7.org/CodeSystem/v3-ParticipationType"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> InvoiceBuilder:
    return (
        InvoiceBuilder()
        .set_id("inv-1")
        .add_identifier("http://sys.id/ni", "NI-1800")
        .set_status("issued")
        .set_cancelled_reason("Pembatalan oleh pasien")
        .set_type("http://terminology.hl7.org/CodeSystem/invoice-type", "inpatient", "Rawat Inap")
        .set_date("2026-01-06T12:00:00+07:00")
        .set_participant(PART, "PPRF", "Practitioner/1000000002", "dr. Budi")
        .set_participant(PART, "ORG", "Organization/1000000001")
        .set_issuer("Organization/1000000001")
        .set_customer("Patient/1000000001")
        .set_account("Account/acc-1")
        .add_line_item(1, KFA, "93000515", "Amoksisilin", 10.0, 15000.0, 1.0)
        .add_line_item(2, PROC, "PROC-2", "Visite")
        .add_line_item_price_component(0, "base", 150000.0)
        .add_line_item_price_component(0, "discount", -5000.0, "DISC")
        .add_line_item_price_component(1, "base", 150000.0)
        .set_total_net(295000.0)
        .set_total_gross(300000.0)
        .set_total_vat(5000.0, "IDR")
        .set_payment_terms("Pembayaran dalam 14 hari")
        .add_note("Catatan invoice")
        .add_note("Catatan kedua")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("invoice")


def test_set_customer_menulis_subject():
    """Quirk kanon: nama method tidak cocok dengan elemennya."""
    hasil = isi().build()
    assert hasil["subject"] == {"reference": "Patient/1000000001"}
    assert "customer" not in hasil


def test_set_code_alias_kini_menulis_type_bukan_code():
    hasil = InvoiceBuilder().set_code("http://x/sys", "C1", "Tampilan").build()
    assert "code" not in hasil
    assert hasil["type"]["coding"][0] == {"system": "http://x/sys", "code": "C1", "display": "Tampilan"}


def test_price_component_menempel_pada_line_item_yang_benar():
    line = isi().build()["lineItem"]
    assert [c["type"] for c in line[0]["priceComponent"]] == ["base", "factor", "base", "discount"]
    assert [c["type"] for c in line[1]["priceComponent"]] == ["base"]


def test_payment_terms_string_bukan_objek():
    assert isi().build()["paymentTerms"] == "Pembayaran dalam 14 hari"


def test_total_net_tanpa_currency_memakai_idr():
    assert InvoiceBuilder().set_total_net(1000.0).build()["totalNet"] == {"value": 1000.0, "currency": "IDR"}
