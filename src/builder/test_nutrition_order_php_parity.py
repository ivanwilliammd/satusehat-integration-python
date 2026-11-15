"""NutritionOrder: 15 setter PHP."""
import json
from pathlib import Path

from src.builder.nutrition_order import NutritionOrderBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> NutritionOrderBuilder:
    return (
        NutritionOrderBuilder()
        .set_id("no-1")
        .add_identifier("http://sys.id/ni", "NI-1900")
        .set_status("active")
        .set_intent("order")
        .set_patient("Patient/1000000001")
        .set_encounter("Encounter/enc-1")
        .set_date_time("2026-01-06T08:00:00+07:00")
        .set_orderer("Practitioner/1000000002")
        .add_allergy_type({"coding": [{"system": "http://sys.id/alergi", "code": "A1", "display": "Seafood"}], "text": "Alergi seafood"})
        .add_food_preference_modifier({"coding": [{"system": "http://hl7.org/fhir/diet", "code": "VEG", "display": "Vegetarian"}]})
        .add_exclude_food_modifier({"text": "Kacang"})
        .set_oral_diet_type({"coding": [{"system": "http://sys.id/diet", "code": "RG", "display": "Rendah Garam"}], "text": "Diet rendah garam"})
        .set_oral_diet_type({"text": "Diet lunak"})
        .add_oral_diet_schedule({"repeat": {"frequency": 3, "period": 1, "periodUnit": "d"}})
        .add_supplement({"type": {"text": "Suplemen zat besi"}, "productName": "Ferrous"})
        .set_enteral_formula({"baseFormulaType": {"text": "Formula standar"}, "caloricDensity": {"value": 1.0}})
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("nutrition_order")


def test_oral_diet_type_menumpuk_dua_kali():
    """Dinamai `set`, tetapi R4 oralDiet.type 0..* — kanon menumpuk."""
    assert len(isi().build()["oralDiet"]["type"]) == 2


def test_oral_diet_schedule_berada_di_dalam_oral_diet():
    oral = isi().build()["oralDiet"]
    assert "schedule" not in isi().build()
    assert oral["schedule"][0]["repeat"]["frequency"] == 3


def test_quirk_allergy_type_bukan_elemen_r4():
    """R4 memakai allergyIntolerance bertipe Reference; kanon menulis allergyType."""
    hasil = isi().build()
    assert "allergyType" in hasil
    assert "allergyIntolerance" not in hasil


def test_alias_lama_tetap_jalan():
    assert NutritionOrderBuilder().status("active").build()["status"] == "active"
