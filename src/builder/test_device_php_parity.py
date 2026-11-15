"""Device: 12 setter PHP, plus cacat nama elemen yang dibetulkan."""
import json
from pathlib import Path

from src.builder.device import DeviceBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> DeviceBuilder:
    monitor = {"coding": [{"system": "http://snomed.info/sct", "code": "26763009", "display": "Monitor"}], "text": "Monitor"}
    return (
        DeviceBuilder()
        .set_id("dev-1")
        .add_identifier("http://sys.id/ni", "NI-2100")
        .set_status("active")
        .set_manufacturer("Philips")
        .add_device_name("Monitor Pasien", "user-friendly-name")
        .add_device_name("M-1234", "model-name")
        .set_type(monitor)
        .set_patient("Patient/1000000001")
        .set_owner("Organization/1000000001")
        .set_location("Location/loc-1")
        .set_serial_number("SN-999")
        .add_note("Catatan perangkat")
        .add_note({"author": "dr. Ani", "time": "2026-01-06", "text": "Diperiksa"})
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("device")


def test_manufacturer_bukan_manufacturer_string():
    """Dulu menulis `manufacturerString`; elemen itu tidak ada di R4."""
    hasil = isi().build()
    assert hasil["manufacturer"] == "Philips"
    assert "manufacturerString" not in hasil


def test_default_device_name_memakai_kode_r4():
    """`user-defined-name` bukan kode R4; kanon memakai `user-friendly-name`."""
    nama = DeviceBuilder().add_device_name("Monitor").build()["deviceName"]
    assert nama[0]["type"] == "user-friendly-name"


def test_status_reason_menimpa_bukan_menumpuk():
    """R4: statusReason 0..1."""
    b = DeviceBuilder().status_reason({"text": "satu"}).status_reason({"text": "dua"})
    assert isinstance(b.build()["statusReason"], dict)
    assert b.build()["statusReason"]["text"] == "dua"


def test_tambahan_python_yang_tidak_ada_di_kanon_tetap_jalan():
    hasil = DeviceBuilder().model_number("M1").part_number("P1").url("https://x/1").build()
    assert hasil["modelNumber"] == "M1"
    assert hasil["partNumber"] == "P1"
    assert hasil["url"] == "https://x/1"
