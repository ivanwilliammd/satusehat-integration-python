"""Dua golden kardinalitas yang sebelumnya tidak dirujuk uji mana pun.

Keduanya mengunci perilaku "menumpuk vs menimpa" yang mudah rusak tanpa suara:
- meta.profile ditumpuk dua kali pada Patient;
- InsurancePlan.type menumpuk dua kali (cacat lama: set_type MENIMPA).
"""
import json
from pathlib import Path

from satusehat_integration.builder.insurance_plan import InsurancePlanBuilder
from satusehat_integration.builder.patient import PatientBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_php_golden.json").read_text())


def test_meta_profile_menumpuk_dua_kali():
    b = (
        PatientBuilder()
        .set_id("Patient/1000000001")
        .set_meta_profile("http://example.org/p1")
        .set_meta_profile("http://example.org/p2")
    )
    assert b.build() == golden("meta_profile_two")


def test_insurance_plan_type_menumpuk_dua_kali():
    b = (
        InsurancePlanBuilder()
        .set_id("ip-2")
        .set_type("http://terminology.hl7.org/CodeSystem/insurance-plan-type", "medical", "Medical")
        .set_type("http://terminology.hl7.org/CodeSystem/insurance-plan-type", "dental", "Dental")
    )
    assert b.build() == golden("insurance_plan_two_types")
