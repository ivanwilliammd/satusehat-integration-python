"""PractitionerRole: 16 setter PHP."""
import json
from pathlib import Path

from src.builder.practitioner_role import PractitionerRoleBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> PractitionerRoleBuilder:
    dokter = {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/practitioner-role", "code": "doctor", "display": "Doctor"}], "text": "Dokter Spesialis"}
    return (
        PractitionerRoleBuilder()
        .set_id("pr-1")
        .add_identifier("http://sys.id/ni", "NI-2200")
        .set_active(True)
        .set_practitioner("Practitioner/1000000002")
        .set_organization("Organization/1000000001")
        .add_code(dokter)
        .add_code({"text": "Dokter Umum"})
        .add_specialty({"coding": [{"system": "http://snomed.info/sct", "code": "394814009", "display": "General practice"}]})
        .add_location("Location/loc-1")
        .add_healthcare_service("HealthcareService/hs-1")
        .add_telecom("phone", "08123456789", "work")
        .add_available_time(["mon", "tue"], "08:00:00", "16:00:00", "Jam kerja")
        .add_available_time()
        .add_not_available("Cuti tahunan", {"start": "2026-01-10", "end": "2026-01-15"})
        .add_endpoint("Endpoint/ep-1")
        .set_availability_exceptions("Libur nasional")
        .add_extension("http://sys.id/ext", "nilai")
        .add_extension("http://sys.id/ext2", 3, "integer")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("practitioner_role")


def test_code_menumpuk_bukan_menimpa():
    """Dulu `code` menulis satu elemen daftar; R4 0..* dan kanon menumpuk."""
    assert len(isi().build()["code"]) == 2


def test_not_available_memakai_during_bukan_period():
    na = isi().build()["notAvailable"][0]
    assert na["during"] == {"start": "2026-01-10", "end": "2026-01-15"}
    assert "period" not in na


def test_available_time_tanpa_argumen_tetap_ditulis_kosong():
    """Quirk kanon: availableTime kosong tetap ditumpuk sebagai [], bukan dilewati."""
    assert isi().build()["availableTime"][1] == []


def test_quirk_description_di_dalam_available_time():
    """R4 tidak punya availableTime.description; kanon menulisnya."""
    assert isi().build()["availableTime"][0]["description"] == "Jam kerja"
