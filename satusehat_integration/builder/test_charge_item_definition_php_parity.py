"""ChargeItemDefinition: 14 setter PHP."""
import json
from pathlib import Path

from satusehat_integration.builder.charge_item_definition import ChargeItemDefinitionBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> ChargeItemDefinitionBuilder:
    return (
        ChargeItemDefinitionBuilder()
        .set_id("cid-1")
        .add_identifier("http://sys.id/ni", "NI-1100")
        .set_url("https://fhir.kemkes.go.id/ChargeItemDefinition/tindakan-1")
        .set_version("1.0.0")
        .set_name("Tarif Tindakan Rawat Jalan")
        .set_title("Tarif Tindakan")
        .set_status("active")
        .set_date("2026-01-01")
        .set_publisher("RS Contoh")
        .set_description("Definisi tarif tindakan rawat jalan")
        .set_code("http://terminology.kemkes.go.id/CodeSystem/procedure", "PROC-1", "Konsultasi")
        .add_instance("ChargeItem/ci-1", "Konsultasi umum", "2026-01-05T09:00:00+07:00")
        .add_instance(None, "Tanpa referensi")
        .add_property("http://snomed.info/sct", "123", "Nilai")
        .add_applies("DateTime", "2026-01-01")
        .add_applies("Age", "18")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("charge_item_definition")


def test_instance_menumpuk_dan_reference_opsional():
    instance = isi().build()["instance"]
    assert len(instance) == 2
    assert instance[0]["reference"] == {"reference": "ChargeItem/ci-1"}
    assert "reference" not in instance[1]


def test_quirk_display_di_tingkat_instance():
    """R4 menaruh display di dalam Reference; PHP menaruhnya di tingkat instance."""
    assert isi().build()["instance"][0]["display"] == "Konsultasi umum"


def test_add_applies_membentuk_nama_elemen_camel():
    hasil = isi().build()
    assert hasil["appliesDateTime"] == "2026-01-01"
    assert hasil["appliesAge"] == "18"


def test_alias_lama_tetap_jalan():
    assert ChargeItemDefinitionBuilder().url("https://x/1").build()["url"] == "https://x/1"
