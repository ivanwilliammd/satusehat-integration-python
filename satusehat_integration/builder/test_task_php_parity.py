"""Task: 26 setter PHP, dengan golden yang dibuat dari skrip PHP bertipe."""
import json
from pathlib import Path

import pytest

from satusehat_integration.builder.task import TaskBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"
TASK_CODE = "http://terminology.hl7.org/CodeSystem/task-code"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def kode_dengan_teks(system, code, display, text):
    hasil = {"coding": [{"system": system, "code": code, "display": display}], "text": text}
    return hasil


CODE = kode_dengan_teks(TASK_CODE, "verify", "Verify", "Verifikasi klaim")


def isi() -> TaskBuilder:
    return (
        TaskBuilder()
        .set_id("task-1")
        .add_identifier("http://sys.id/ni", "NI-1400")
        .add_identifier("http://sys.id/lain", "LAIN-1")
        .set_instantiates_canonical("https://fhir.kemkes.go.id/Task/t1")
        .set_instantiates_uri("urn:uuid:1")
        .set_status("requested")
        .set_status_reason({"coding": [{"system": "http://sys.id/status-reason", "code": "SR1"}], "text": "Belum lengkap"})
        .set_business_status({"coding": [{"system": "http://sys.id/business", "code": "B1", "display": "Menunggu"}]})
        .set_intent("order")
        .set_priority("urgent")
        .set_code(CODE)
        .set_description("Verifikasi data klaim")
        .set_focus("qr-1", "Kuesioner")
        .set_for("1000000001", "Budi Santoso")
        .set_encounter("enc-1")
        .set_execution_period("2026-01-05", "2026-01-06")
        .set_authored_on("2026-01-05T08:00:00+07:00")
        .set_last_modified("2026-01-05T09:30:00+07:00")
        .set_requester("1000000002", "dr. Budi")
        .set_owner("Practitioner/1000000003", "dr. Ani")
        .set_location("loc-1", "Rawat Jalan")
        .set_reason_code(CODE)
        .set_reason_reference("Condition/cond-1")
        .add_input("Jumlah", "10")
        .add_input(CODE, 5)
        .add_output(CODE, "selesai")
        .add_restriction("1000000002", 3, {"start": "2026-01-05", "end": "2026-01-10"})
        .add_restriction("Practitioner/1000000004")
        .add_note("Catatan tugas")
        .add_extension("http://sys.id/ext", "nilai")
        .add_extension("http://sys.id/ext2", 5, "integer")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("task")


def test_reason_code_dan_reference_bukan_daftar():
    """Sebelumnya dua setter ini menumpuk; R4 menuntut satu nilai (0..1)."""
    hasil = isi().build()
    assert isinstance(hasil["reasonCode"], dict)
    assert isinstance(hasil["reasonReference"], dict)


def test_alias_lama_add_reason_menimpa_bukan_menumpuk():
    b = TaskBuilder().add_reason_code(CODE).add_reason_code(CODE)
    assert isinstance(b.build()["reasonCode"], dict)


def test_reference_tanpa_garis_miring_diberi_awalan_resource():
    hasil = isi().build()
    assert hasil["focus"]["reference"] == "QuestionnaireResponse/qr-1"
    assert hasil["for"]["reference"] == "Patient/1000000001"
    assert hasil["encounter"]["reference"] == "Encounter/enc-1"


def test_quirk_restriction_selalu_berawalan_patient():
    """PHP memberi awalan Patient/ bahkan untuk id Practitioner — ditiru apa adanya."""
    assert isi().build()["restriction"][0]["requester"]["reference"] == "Patient/1000000002"


def test_extension_memakai_value_type_bila_diberi():
    ext = isi().build()["extension"]
    assert ext[0] == {"url": "http://sys.id/ext", "valueString": "nilai"}
    assert ext[1] == {"url": "http://sys.id/ext2", "valueInteger": 5}


def test_status_dan_intent_menolak_nilai_asing():
    with pytest.raises(ValueError):
        TaskBuilder().set_status("selesai")
    with pytest.raises(ValueError):
        TaskBuilder().set_intent("perintah")
