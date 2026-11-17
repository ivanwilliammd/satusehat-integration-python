"""ChargeItemResponse: resource rumahan (bukan R4), 14 setter."""
import json
from pathlib import Path

from satusehat_integration.builder.charge_item_response import ChargeItemResponseBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> ChargeItemResponseBuilder:
    return (
        ChargeItemResponseBuilder()
        .set_id("cir-1")
        .add_identifier("http://sys.id/ni", "NI-1200")
        .set_status("completed")
        .set_charge_item("ChargeItem/ci-1")
        .set_part_of("Encounter/enc-1")
        .set_request("ServiceRequest/sr-1")
        .set_outcome("http://terminology.hl7.org/CodeSystem/chargeitem-response", "approved", "Disetujui")
        .set_description("Persetujuan biaya tindakan")
        .set_created("2026-01-06T11:00:00+07:00")
        .set_requestor("Practitioner/1000000002")
        .add_outcome_info("http://sys.id/outcome", "OK", "Sesuai")
        .add_error("http://sys.id/error", "E1", "Kode tidak dikenal")
        .add_cost_center_charge_item_response("Organization/1000000001", "Rawat Jalan")
        .set_response_date("2026-01-06")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("charge_item_response")


def test_resource_type_bukan_r4():
    """Nilai ini sengaja diuji: kalau resourceType berubah, artinya kanon berubah."""
    assert isi().build()["resourceType"] == "ChargeItemResponse"


def test_part_of_menumpuk_dan_charge_item_menimpa():
    hasil = isi().build()
    assert isinstance(hasil["partOf"], list)
    assert hasil["chargeItem"] == {"reference": "ChargeItem/ci-1"}


def test_outcome_info_dan_error_berbentuk_code():
    hasil = isi().build()
    assert hasil["outcomeInfo"][0]["code"]["coding"][0]["code"] == "OK"
    assert hasil["error"][0]["code"]["coding"][0]["code"] == "E1"


def test_cost_center_menyertakan_display_bila_diberi():
    hasil = isi().build()
    assert hasil["costCenterChargeItemResponse"][0]["costCenter"] == {
        "reference": "Organization/1000000001",
        "display": "Rawat Jalan",
    }
