"""Enam modul yang permukaannya paling dekat dengan PHP.

Golden dibuat dari builder PHP lewat runner. Yang diuji hanya method yang ada di
kedua sisi dengan bentuk yang sama; method yang belum ada di Python tidak
dipalsukan di sini — itu dicatat di docs/PARITY.md sebagai selisih.
"""
import json
from pathlib import Path

import pytest

from src.builder.account import AccountBuilder
from src.builder.adverse_event import AdverseEventBuilder
from src.builder.appointment import AppointmentBuilder
from src.builder.appointment_response import AppointmentResponseBuilder
from src.builder.molecular_sequence import MolecularSequenceBuilder
from src.builder.risk_assessment import RiskAssessmentBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def akun():
    return (
        AccountBuilder()
        .set_id("acc-2")
        .set_status("active")
        .set_name("Akun Rawat Inap")
        .set_service_period("2026-01-05", "2026-01-07")
        .set_description("Akun rawat inap")
        .set_owner("Organization/1000000001")
    )


def kejadian():
    return (
        AdverseEventBuilder()
        .set_id("ae-1")
        .add_identifier("http://sys.id/ni", "NI-800")
        .set_status("active")
        .set_code("http://snomed.info/sct", "42284007", "Reaksi transfusi")
        .set_subject("Patient/1000000001")
    )


def janji():
    return (
        AppointmentBuilder()
        .set_id("appt-1")
        .add_identifier("http://sys.id/ni", "NI-801")
        .set_status("booked")
        .set_code("http://snomed.info/sct", "185389009", "Kunjungan")
        .set_subject("Patient/1000000001")
    )


def jawaban_janji():
    return (
        AppointmentResponseBuilder()
        .set_id("ar-1")
        .add_identifier("http://sys.id/ni", "NI-802")
        .set_status("accepted")
        .set_code("http://snomed.info/sct", "185389009", "Kunjungan")
        .set_subject("Patient/1000000001")
    )


def urutan():
    return MolecularSequenceBuilder().set_coordinate_system(0).set_id("ms-2")


def penilaian():
    return (
        RiskAssessmentBuilder()
        .set_id("ra-2")
        .set_status("final")
        .set_mitigation("Antibiotik dalam 1 jam")
    )


KASUS = {
    "account": (akun, "account"),
    "adverse_event": (kejadian, "adverse_event"),
    "appointment": (janji, "appointment"),
    "appointment_response": (jawaban_janji, "appointment_response"),
    "molecular_sequence": (urutan, "molecular_sequence"),
    "risk_assessment": (penilaian, "risk_assessment"),
}


@pytest.mark.parametrize("nama", list(KASUS), ids=list(KASUS))
def test_sama_dengan_golden_php(nama):
    bangun, berkas = KASUS[nama]
    assert bangun().build() == golden(berkas)


def test_set_code_menerima_tiga_argumen_dan_dict():
    dari_argumen = kejadian().build()["code"]
    dari_dict = (
        AdverseEventBuilder()
        .set_code({"coding": [{"system": "http://snomed.info/sct", "code": "42284007", "display": "Reaksi transfusi"}]})
        .build()["code"]
    )
    assert dari_argumen == dari_dict
