"""QuestionnaireResponse: 9 setter PHP."""
import json
from pathlib import Path

import pytest

from src.builder.questionnaire_response import QuestionnaireResponseBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> QuestionnaireResponseBuilder:
    ya = {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0136", "code": "Y", "display": "Yes"}], "text": "Ya"}
    return (
        QuestionnaireResponseBuilder()
        .set_id("qr-1")
        .set_status("COMPLETED")
        .set_questionnaire("https://fhir.kemkes.go.id/r4/Questionnaire/skrining")
        .set_subject("Patient/1000000001")
        .set_encounter("Encounter/enc-1")
        .set_authored("2026-01-05T10:00:00+07:00")
        .set_author("Practitioner/1000000002")
        .set_source("Patient/1000000001")
        .add_item("1.1", "Apakah demam?", ya)
        .add_item("1.2", None, {"text": "Tidak"})
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("questionnaire_response")


def test_questionnaire_canonical_bukan_reference():
    """R4: questionnaire bertipe canonical; dulu Python menulis {'reference': …}."""
    hasil = isi().build()
    assert isinstance(hasil["questionnaire"], str)
    assert hasil["questionnaire"].startswith("https://fhir.kemkes.go.id/")


def test_status_huruf_besar_dinormalkan_dan_divalidasi():
    assert QuestionnaireResponseBuilder().set_status("Amended").build()["status"] == "amended"
    with pytest.raises(ValueError):
        QuestionnaireResponseBuilder().set_status("selesai")


def test_status_default_completed_saat_build():
    assert QuestionnaireResponseBuilder().build()["status"] == "completed"


def test_add_item_membungkus_satu_jawaban_di_dalam_daftar():
    """Quirk kanon: satu item hanya bisa memuat satu jawaban meski R4 mengizinkan 0..*."""
    item = isi().build()["item"]
    assert isinstance(item[0]["answer"], list) and len(item[0]["answer"]) == 1
    assert "text" not in item[1]
