"""ChargeItem: 23 setter PHP, dibandingkan dengan golden yang dibuat dari PHP."""
import json
from pathlib import Path

from satusehat_integration.builder.charge_item import ChargeItemBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"
DICOM = "http://dicom.nema.org/resources/ontology/DCM"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> ChargeItemBuilder:
    return (
        ChargeItemBuilder()
        .set_id("ci-1")
        .add_identifier("http://sys.id/ni", "NI-200")
        .add_identifier("http://sys.id/rm", "RM-9")
        .set_status("billable")
        .set_part_of("Encounter/enc-1")
        .set_code("http://terminology.kemkes.go.id/CodeSystem/procedure", "PROC-1", "Konsultasi")
        .set_subject("Patient/1000000001")
        .set_focus("Procedure/proc-1")
        .set_encounter("Encounter/enc-1")
        .set_performed_date("2026-01-05T09:00:00+07:00")
        .set_performer_actor(
            "Practitioner/1000000002",
            "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
            "PPRF",
        )
        .set_performer_cost_center("Organization/1000000001")
        .set_organization("Organization/1000000001")
        .set_requesting_organization("Organization/1000000002")
        .set_quantity(3)
        .set_bodysite("http://snomed.info/sct", "123", "Toraks")
        .set_product_code("http://sys-ids.kemkes.go.id/kfa", "93000515", "Amoksisilin")
        .set_price_override(150000.0, "IDR")
        .set_override_reason("Harga khusus peserta")
        .set_enterer("Practitioner/1000000003")
        .set_entered_date("2026-01-05T10:00:00+07:00")
        .set_reason("http://snomed.info/sct", "456", "Tindakan")
        .set_service("ServiceRequest/sr-1")
        .set_account("Account/acc-1")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("charge_item")


def test_encounter_menulis_context_bukan_encounter():
    hasil = isi().build()
    assert hasil["context"] == {"reference": "Encounter/enc-1"}
    assert "encounter" not in hasil


def test_quantity_ditulis_angka_bukan_objek():
    assert isi().build()["quantity"] == 3


def test_bodysite_menumpuk_sebagai_daftar():
    hasil = isi().build()
    assert isinstance(hasil["bodysite"], list)
    assert hasil["bodysite"][0]["coding"][0]["code"] == "123"


def test_performer_menumpuk_dua_kali():
    assert len(isi().build()["performer"]) == 2
