"""GenomicStudy: resource non-R4-inti, 15 setter PHP."""
import json
from pathlib import Path

import pytest

from satusehat_integration.builder.genomic_study import PARTICIPATION, GenomicStudyBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> GenomicStudyBuilder:
    return (
        GenomicStudyBuilder()
        .set_meta_profile("https://fhir.kemkes.go.id/r4/StructureDefinition/GenomicStudy")
        .set_id("gs-1")
        .add_identifier("http://sys.id/ni", "NI-1700")
        .set_status("available")
        .add_type({"text": "WES"})
        .add_type({"coding": [{"system": "http://sys.id/type", "code": "T2", "display": "Tipe 2"}]})
        .set_subject("Patient/1000000001")
        .set_encounter("Encounter/enc-1")
        .set_start_date("2026-01-05T09:00:00+07:00")
        .add_based_on("ServiceRequest/sr-1")
        .set_referrer("Practitioner/1000000002")
        .add_interpreter("Practitioner/1000000003")
        .add_reason({"text": "Riwayat keluarga"})
        .add_note("Catatan genomik")
        .add_note({"author": "dr. Ani", "time": "2026-01-06", "text": "Ditelaah"})
        .set_description("Whole exome sequencing")
        .add_analysis({"description": "Analisis WES", "status": "completed"})
        .add_performer("Practitioner/1000000004")
        .add_performer("Organization/1000000001", "ORG")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("genomic_study")


def test_start_date_bukan_started():
    """Dulu Python menulis `started`; kanon menulis `startDate`, jadi nilainya tak terbaca."""
    hasil = isi().build()
    assert hasil["startDate"] == "2026-01-05T09:00:00+07:00"
    assert "started" not in hasil


def test_type_menumpuk_bukan_menimpa():
    assert len(isi().build()["type"]) == 2


def test_tiga_nilai_status_di_luar_daftar_ditolak():
    for salah in ["active", "ACTIVE", ""]:
        with pytest.raises(ValueError):
            GenomicStudyBuilder().set_status(salah)


def test_performer_memakai_role_perf_default():
    performer = isi().build()["performer"]
    assert performer[0]["role"]["coding"][0] == {
        "system": PARTICIPATION,
        "code": "PERF",
        "display": "Performer",
    }


def test_alias_lama_ikut_dibetulkan():
    b = GenomicStudyBuilder().started("2026-01-05").type({"text": "WGS"}).type({"text": "WES"})
    hasil = b.build()
    assert hasil["startDate"] == "2026-01-05"
    assert len(hasil["type"]) == 2
