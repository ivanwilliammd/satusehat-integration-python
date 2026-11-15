"""Group: 12 setter PHP, termasuk cacat kunci literal "meta/profile" yang kini dibetulkan."""
import json
from pathlib import Path

from src.builder.group import GroupBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> GroupBuilder:
    keluarga = {"coding": [{"system": "http://snomed.info/sct", "code": "35359004", "display": "Family"}], "text": "Keluarga"}
    return (
        GroupBuilder()
        .set_meta_profile("https://fhir.kemkes.go.id/r4/StructureDefinition/Group")
        .set_meta_profile("https://fhir.kemkes.go.id/r4/StructureDefinition/Group2")
        .set_id("grp-1")
        .add_identifier("http://sys.id/ni", "NI-1600")
        .add_identifier({"system": "http://sys.id/lain", "value": "LAIN-2"})
        .set_active(True)
        .set_type("person")
        .set_actual(True)
        .set_code(keluarga)
        .set_name("Keluarga Budi")
        .set_quantity(3)
        .set_managing_entity({"reference": "Organization/1000000001"})
        .add_member("1000000001", "Budi Santoso", {"start": "2026-01-01"}, False)
        .add_member("Patient/1000000002", None, False)
        .add_member({"reference": "Practitioner/1000000003"}, {"start": "2026-01-02"})
        .add_member("1000000004")
        .add_extension("http://sys.id/ext-bool", True)
        .add_extension("http://sys.id/ext-str", "nilai")
        .add_extension("http://sys.id/ext-int", 7)
        .add_extension("http://sys.id/ext-arr", {"valueCode": "X"})
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("group")


def test_meta_profile_bukan_kunci_literal():
    """Dulu kunci "meta/profile" ditulis apa adanya: JSON sah, tetapi tidak dibaca server."""
    hasil = isi().build()
    assert "meta/profile" not in hasil
    assert hasil["meta"]["profile"] == [
        "https://fhir.kemkes.go.id/r4/StructureDefinition/Group",
        "https://fhir.kemkes.go.id/r4/StructureDefinition/Group2",
    ]


def test_member_menerima_empat_bentuk_argumen():
    member = isi().build()["member"]
    assert member[0]["entity"] == {"reference": "Patient/1000000001", "display": "Budi Santoso"}
    assert member[0]["period"] == {"start": "2026-01-01"}
    assert member[0]["inactive"] is False
    assert member[1] == {"entity": {"reference": "Patient/1000000002"}, "inactive": False}
    assert member[2]["entity"]["reference"] == "Practitioner/1000000003"
    assert "inactive" not in member[2]
    assert member[3] == {"entity": {"reference": "Patient/1000000004"}}


def test_extension_memilih_value_menurut_tipe():
    ext = isi().build()["extension"]
    assert ext[0]["valueBoolean"] is True
    assert ext[1]["valueString"] == "nilai"
    assert ext[2]["valueInteger"] == 7
    assert ext[3]["valueCode"] == "X"
