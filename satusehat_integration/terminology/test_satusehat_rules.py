"""Uji aturan wajib SATUSEHAT.

Sumbernya data/satusehat/required-rules.json, bukan ingatan: uji terakhir memastikan modul hasil
generate masih sama dengan JSON-nya, sehingga JSON tidak bisa disunting tanpa artefak ikut berubah.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

from satusehat_integration.terminology._rules_generated import RULES, RULES_SHA
from satusehat_integration.terminology.satusehat_rules import (
    ACT_CODE,
    ENCOUNTER_STATUS,
    OBSERVATION_STATUS,
    PROCEDURE_STATUS,
    violations,
)

AKAR = pathlib.Path(__file__).resolve().parent.parent.parent


def _encounter(system: str, status: str = "finished") -> dict:
    return {"resourceType": "Encounter", "status": status, "class": {"system": system, "code": "AMB"}}


def test_encounter_dengan_v3_actcode_lolos() -> None:
    assert violations(_encounter(ACT_CODE)) == []


def test_encounter_dengan_sistem_lain_ditolak() -> None:
    masalah = violations(_encounter("http://contoh.local/class"))
    assert len(masalah) == 1
    assert "v3-ActCode" in masalah[0]


def test_status_di_luar_daftar_ditolak() -> None:
    assert "bukan kode yang sah" in violations(_encounter(ACT_CODE, "selesai"))[0]


def test_observation_tanpa_encounter_menyebut_alasan_r4() -> None:
    masalah = violations({
        "resourceType": "Observation",
        "status": "final",
        "code": {"coding": [{"system": "http://loinc.org", "code": "8867-4"}]},
        "subject": {"reference": "Patient/1"},
    })
    assert len(masalah) == 1
    assert "opsional di R4" in masalah[0]


def test_subject_bukan_patient_ditolak() -> None:
    masalah = violations({
        "resourceType": "Condition",
        "code": {"coding": [{"system": "http://hl7.org/fhir/sid/icd-10", "code": "E11.9"}]},
        "subject": {"reference": "Group/1"},
        "encounter": {"reference": "Encounter/2"},
    })
    assert len(masalah) == 1
    assert "Patient" in masalah[0]


def test_patient_wajib_punya_nama() -> None:
    masalah = violations({
        "resourceType": "Patient",
        "identifier": [{"system": "https://fhir.kemkes.go.id/id/nik", "value": "3273010101900001"}],
    })
    assert len(masalah) == 1
    assert "name" in masalah[0]


def test_immunization_menerima_occurrence_datetime_dan_string() -> None:
    dasar = {
        "resourceType": "Immunization",
        "status": "completed",
        "vaccineCode": {"coding": [{"system": "http://hl7.org/fhir/sid/cvx", "code": "08"}]},
        "patient": {"reference": "Patient/1"},
    }
    assert violations({**dasar, "occurrenceDateTime": "2026-11-16T09:00:00+07:00"}) == []
    assert violations({**dasar, "occurrenceString": "2026-11-16"}) == []
    assert "occurrenceDateTime" in violations(dasar)[0]


def test_medication_request_wajib_intent() -> None:
    masalah = violations({
        "resourceType": "MedicationRequest",
        "status": "active",
        "subject": {"reference": "Patient/1"},
    })
    assert len(masalah) == 1
    assert "intent" in masalah[0]


def test_resource_tak_dipetakan_tidak_diperiksa() -> None:
    assert violations({"resourceType": "AuditEvent"}) == []


def test_tanpa_resource_type_dilaporkan() -> None:
    assert violations({"status": "finished"}) == ["resourceType tidak ada"]


def test_setiap_butir_menyebut_sumber_dan_jenis_dikenal() -> None:
    jenis = {"kode", "isi", "ada", "referensi", "sistem", "salah_satu"}
    for resource, butir in RULES.items():
        assert butir, f"{resource} tanpa aturan"
        for satu in butir:
            assert satu.get("sumber"), f"{resource} tanpa sumber"
            assert satu["jenis"] in jenis, f"{resource} jenis tak dikenal"


def test_konstanta_sama_dengan_berkas_aturan() -> None:
    def kode(resource: str) -> list[str]:
        for butir in RULES[resource]:
            if butir["elemen"] == "status" and butir["jenis"] == "kode":
                return butir["kode"]
        return []

    assert kode("Encounter") == list(ENCOUNTER_STATUS)
    assert kode("Observation") == list(OBSERVATION_STATUS)
    assert kode("Procedure") == list(PROCEDURE_STATUS)


def test_artefak_generate_masih_sama_dengan_json() -> None:
    mentah = (AKAR / "data" / "satusehat" / "required-rules.json").read_bytes()
    assert hashlib.sha256(mentah).hexdigest()[:16] == RULES_SHA, (
        "JSON berubah tanpa generate: jalankan python3 scripts/generate_rules.py"
    )
    isi = json.loads(mentah.decode("utf-8"))
    badan = {k: v for k, v in isi.items() if not k.startswith("_") and isinstance(v, list)}
    assert badan == RULES
