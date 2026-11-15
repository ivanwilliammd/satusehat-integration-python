"""EpisodeOfCare: 15 setter PHP, termasuk diagnosis.role yang sebelumnya hilang."""
import json
from pathlib import Path

import pytest

from src.builder.episode_of_care import EpisodeOfCareBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> EpisodeOfCareBuilder:
    rajal = {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/episodeofcare-type", "code": "hacc", "display": "Home and Community Care"}], "text": "Rawat Jalan"}
    peran = {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/diagnosis-role", "code": "CC", "display": "Chief complaint"}], "text": "Diagnosis utama"}
    return (
        EpisodeOfCareBuilder()
        .set_id("eoc-1")
        .add_identifier("http://sys.id/ni", "NI-2300")
        .set_status("active")
        .add_status_history("planned", "2026-01-01", "2026-01-02")
        .add_status_history("active", "2026-01-02")
        .set_patient("Patient/1000000001")
        .set_managing_organization("Organization/1000000001")
        .add_type(rajal)
        .add_type({"text": "Rawat Inap"})
        .set_period({"start": "2026-01-01", "end": "2026-01-31"})
        .add_diagnosis("Condition/cond-1", peran, 1)
        .add_referral_request("ServiceRequest/sr-1")
        .set_care_manager("Practitioner/1000000002")
        .add_team("CareTeam/ct-1")
        .add_account("Account/acc-1")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("episode_of_care")


def test_diagnosis_memuat_role_yang_wajib_di_r4():
    """R4: diagnosis.role 1..1; versi Python sebelumnya tidak pernah menulisnya."""
    diagnosis = isi().build()["diagnosis"][0]
    assert diagnosis["role"]["coding"][0]["code"] == "CC"
    assert diagnosis["condition"] == {"reference": "Condition/cond-1"}
    assert diagnosis["rank"] == 1


def test_type_menumpuk_bukan_menimpa():
    assert len(isi().build()["type"]) == 2


def test_status_tidak_sah_ditolak_di_dua_setter():
    with pytest.raises(ValueError):
        EpisodeOfCareBuilder().set_status("open")
    with pytest.raises(ValueError):
        EpisodeOfCareBuilder().add_status_history("open", "2026-01-01")


def test_alias_lama_status_history_menerima_objek_period():
    hasil = EpisodeOfCareBuilder().status_history("active", {"start": "2026-01-01"}).build()
    assert hasil["statusHistory"][0]["period"] == {"start": "2026-01-01"}
