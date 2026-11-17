"""ClinicalImpression: 19 setter PHP."""
import json
from pathlib import Path

from satusehat_integration.builder.clinical_impression import ClinicalImpressionBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> ClinicalImpressionBuilder:
    asesmen = {"coding": [{"system": "http://sys.id/asesmen", "code": "A1", "display": "Asesmen"}], "text": "Asesmen awal"}
    demam = {"coding": [{"system": "http://snomed.info/sct", "code": "386661006", "display": "Fever"}], "text": "Demam"}
    return (
        ClinicalImpressionBuilder()
        .set_id("ci-1")
        .add_identifier("http://sys.id/ni", "NI-2000")
        .set_status("completed")
        .set_code(asesmen)
        .set_subject("Patient/1000000001")
        .set_encounter("Encounter/enc-1")
        .set_effective_date_time("2026-01-05T09:00:00+07:00")
        .set_effective_period({"start": "2026-01-05", "end": "2026-01-06"})
        .set_date("2026-01-06")
        .set_assessor("Practitioner/1000000002")
        .set_previous_opinion("ClinicalImpression/ci-0")
        .add_investigation({"code": {"text": "Pemeriksaan lab"}, "item": [{"reference": "Observation/obs-1"}]})
        .add_finding_codeable_concept(demam)
        .add_finding_reference("Observation/obs-2")
        .add_prognosis_codeable_concept({"text": "Prognosis baik"})
        .add_prognosis_reference("RiskAssessment/ra-1")
        .add_supporting_info("Observation/obs-3")
        .add_note("Catatan pertama")
        .add_note({"author": "dr. Ani", "time": "2026-01-06", "text": "Catatan anotasi"})
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("clinical_impression")


def test_note_menumpuk_bukan_menimpa():
    """Alias lama `note()` dulu menimpa seluruh daftar; kini menumpuk seperti kanon."""
    assert len(isi().build()["note"]) == 2
    dua = ClinicalImpressionBuilder().note("satu").note("dua").build()
    assert [n["text"] for n in dua["note"]] == ["satu", "dua"]


def test_quirk_previous_opinion_bukan_previous():
    hasil = isi().build()
    assert hasil["previousOpinion"] == {"reference": "ClinicalImpression/ci-0"}
    assert "previous" not in hasil


def test_finding_menerima_dua_bentuk():
    finding = isi().build()["finding"]
    assert "itemCodeableConcept" in finding[0]
    assert finding[1]["itemReference"] == {"reference": "Observation/obs-2"}


def test_summary_tambahan_sah_r4_tidak_ditulis_kanon():
    assert "summary" not in isi().build()
    assert ClinicalImpressionBuilder().set_summary("Ringkasan").build()["summary"] == "Ringkasan"
