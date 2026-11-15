"""Claim: 26 setter PHP, dibandingkan dengan golden yang dibuat dari PHP."""
import json
from pathlib import Path

import pytest

from src.builder.claim import ClaimBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"
SYS_ID = "http://sys.id/ni"
KFA = "http://sys-ids.kemkes.go.id/kfa"
ICD10 = "http://hl7.org/fhir/sid/icd-10"
PROC = "http://terminology.kemkes.go.id/CodeSystem/procedure"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> ClaimBuilder:
    return (
        ClaimBuilder()
        .set_id("clm-1")
        .add_identifier(SYS_ID, "NI-500")
        .set_status("active")
        .set_type("http://terminology.hl7.org/CodeSystem/claim-type", "institutional", "Institusi")
        .set_sub_type("http://terminology.hl7.org/CodeSystem/ex-claimsubtype", "subrogation", "Subrogasi")
        .set_use("claim")
        .set_priority("http://terminology.hl7.org/CodeSystem/processpriority", "normal", "Normal")
        .set_patient("Patient/1000000001", "Budi Santoso")
        .set_billable_period("2026-01-05", "2026-01-06")
        .set_created("2026-01-06T10:00:00+07:00")
        .set_enterer("Practitioner/1000000002")
        .set_insurer("Organization/1000000003")
        .set_provider("Organization/1000000001")
        .set_priority_payor("Organization/1000000003")
        .set_priority_payor("Organization/1000000004")
        .set_prescriber("Practitioner/1000000005")
        .set_facility("Location/loc-1", "Rawat Jalan")
        .add_related(
            "http://sys.id/claim-ref",
            "CLM-OLD",
            "Klaim lama",
            "http://terminology.hl7.org/CodeSystem/ex-relatedclaimrelationship",
            "prior",
        )
        .add_coverage("Coverage/cov-1")
        .add_coverage("Coverage/cov-2", False, "http://terminology.hl7.org/CodeSystem/coverage-priority", "2")
        .add_item(1, KFA, "93000515", "Amoksisilin", 1, 1, 1)
        .add_item(2, PROC, "PROC-2", "Visite")
        .add_item_serviced_period(0, "2026-01-05", "2026-01-06")
        .add_item_location(0, "http://sys.id/loc", "LOC-1", "Rawat Jalan")
        .add_item_location(0, "http://sys.id/loc", "LOC-2", "Rawat Inap")
        .add_item_quantity(0, 10.0, "IDR")
        .add_item_unit_price(0, 15000.0, "IDR")
        .add_item_unit_price(1, 150000.0, "IDR")
        .add_care_team(
            1,
            "Practitioner/1000000002",
            "http://terminology.hl7.org/CodeSystem/claimcareteamrole",
            "primary",
            "Dokter Utama",
        )
        .add_diagnosis(1, ICD10, "A09", "http://terminology.hl7.org/CodeSystem/ex-diagnosistype", "principal")
        .add_procedure(1, PROC, "PROC-2", "2026-01-05", "http://terminology.hl7.org/CodeSystem/ex-procedure-type", "primary")
        .add_insurance_account("Account/acc-1")
        .add_insurance_account("Account/acc-2")
        .set_total(315000.0, "IDR")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("claim")


def test_item_kedua_tidak_mewarisi_serviced_period_item_pertama():
    item = isi().build()["item"]
    assert item[0]["servicedPeriod"] == {"start": "2026-01-05", "end": "2026-01-06"}
    assert "servicedPeriod" not in item[1]


def test_item_location_menumpuk():
    assert len(isi().build()["item"][0]["location"]) == 2


def test_add_insurance_account_hanya_menulis_account():
    assert isi().build()["insurance"] == {
        "account": [{"reference": "Account/acc-1"}, {"reference": "Account/acc-2"}]
    }


def test_quirk_quantity_memakai_currency():
    assert isi().build()["item"][0]["quantity"] == {"value": 10.0, "currency": "IDR"}


def test_add_item_memakai_urutan_php_system_dulu():
    """Alias tidak boleh membalik argumen: itu cacat yang baru saja diperbaiki di 22 setter."""
    item = ClaimBuilder().add_item(1, "http://contoh/sistem", "PROC-1", "Konsultasi").build()["item"][0]
    assert item["productOrService"]["coding"][0]["system"] == "http://contoh/sistem"
    assert item["productOrService"]["coding"][0]["code"] == "PROC-1"
