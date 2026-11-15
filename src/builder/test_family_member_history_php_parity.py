"""FamilyMemberHistory: 26 setter PHP, sebelumnya hanya enam method tanpa awalan set_."""
import json
from pathlib import Path

import pytest

from src.builder.family_member_history import FamilyMemberHistoryBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_php_golden.json").read_text())


def cc(system: str, code: str, display: str) -> dict:
    return {"coding": [{"system": system, "code": code, "display": display}]}


def isi() -> FamilyMemberHistoryBuilder:
    rel = cc("http://terminology.hl7.org/CodeSystem/v3-RoleCode", "MTH", "Mother")
    rel["text"] = "Ibu"
    sex = cc("http://hl7.org/fhir/administrative-gender", "female", "Female")
    sex["text"] = "Perempuan"
    hipertensi = cc("http://hl7.org/fhir/sid/icd-10", "I10", "Essential hypertension")
    hipertensi["text"] = "Hipertensi"
    return (
        FamilyMemberHistoryBuilder()
        .set_id("fmh-1")
        .add_identifier("http://sys.id/ni", "NI-1000")
        .set_instantiates_canonical("https://fhir.kemkes.go.id/r4/Questionnaire/family-history")
        .set_status("completed")
        .set_patient("Patient/1000000001", "Budi Santoso")
        .set_date("2026-01-05")
        .set_name("Ibu Kandung")
        .set_relationship(rel)
        .set_sex(sex)
        .set_born_date("1958-03-02")
        .set_age_age(68, "a")
        .set_deceased_boolean(False)
        .add_condition(hipertensi, "2005", None, False)
        .add_condition({"text": "Diabetes melitus tipe 2"})
        .add_reason_reference("Condition/cond-1")
        .set_note("Riwayat keluarga terverifikasi")
        .set_note("Data dari rekam medis ibu")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("family_member_history")


def test_set_note_menumpuk_meski_dinamai_set():
    assert len(isi().build()["note"]) == 2


def test_set_status_menolak_nilai_di_luar_empat_yang_sah():
    with pytest.raises(ValueError):
        FamilyMemberHistoryBuilder().set_status("active")


def test_condition_menumpuk_dan_onset_string_hanya_bila_diberi():
    kondisi = isi().build()["condition"]
    assert len(kondisi) == 2
    assert kondisi[0]["onsetString"] == "2005"
    assert "onsetString" not in kondisi[1]


def test_quirk_age_age_angka_dan_satuan_terpisah():
    hasil = isi().build()
    assert hasil["ageAge"] == 68
    assert hasil["ageUnit"] == "a"


def test_alias_lama_tetap_jalan():
    b = FamilyMemberHistoryBuilder().status("completed").patient("Patient/1000000001")
    hasil = b.build()
    assert hasil["status"] == "completed"
    assert hasil["patient"] == {"reference": "Patient/1000000001"}
