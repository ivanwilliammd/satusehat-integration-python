"""NutritionOrder resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderNutritionOrder.php. Versi sebelumnya hanya lima method tanpa
awalan `set_`; identifier, oralDiet, supplement, enteralFormula, dan tiga setter
CodeableConcept belum ada.

Quirk kanon ditiru dan ditandai: `addAllergyType` menulis `allergyType`, padahal R4
NutritionOrder memakai `allergyIntolerance` yang bertipe Reference (bukan
CodeableConcept), sehingga dua-duanya tidak cocok.
"""
from typing import Any, Dict, Optional

from src.builder.base_builder import BaseBuilder


def _konsep(nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> Dict[str, Any]:
    if isinstance(nilai, dict):
        return nilai
    coding: Dict[str, Any] = {"system": nilai, "code": code or ""}
    if display:
        coding["display"] = display
    return {"coding": [coding]}


class NutritionOrderBuilder(BaseBuilder):
    """Builder for NutritionOrder resource."""

    def __init__(self) -> None:
        super().__init__("NutritionOrder")

    def set_id(self, id: str) -> "NutritionOrderBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "NutritionOrderBuilder":
        if isinstance(identifier, dict):
            return self._push("identifier", identifier)
        return self._push("identifier", {"system": identifier, "value": value})

    def set_status(self, status: str) -> "NutritionOrderBuilder":
        self.data["status"] = status
        return self

    def set_intent(self, intent: str) -> "NutritionOrderBuilder":
        self.data["intent"] = intent
        return self

    def set_patient(self, patient: Any) -> "NutritionOrderBuilder":
        self.data["patient"] = patient if isinstance(patient, dict) else {"reference": patient}
        return self

    def set_encounter(self, encounter: Any) -> "NutritionOrderBuilder":
        self.data["encounter"] = encounter if isinstance(encounter, dict) else {"reference": encounter}
        return self

    def set_date_time(self, date_time: str) -> "NutritionOrderBuilder":
        self.data["dateTime"] = date_time
        return self

    def set_orderer(self, orderer: Any) -> "NutritionOrderBuilder":
        self.data["orderer"] = orderer if isinstance(orderer, dict) else {"reference": orderer}
        return self

    def add_allergy_type(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "NutritionOrderBuilder":
        """Quirk kanon: R4 memakai `allergyIntolerance` bertipe Reference."""
        return self._push("allergyType", _konsep(nilai, code, display))

    def add_food_preference_modifier(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "NutritionOrderBuilder":
        return self._push("foodPreferenceModifier", _konsep(nilai, code, display))

    def add_exclude_food_modifier(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "NutritionOrderBuilder":
        return self._push("excludeFoodModifier", _konsep(nilai, code, display))

    def set_oral_diet_type(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "NutritionOrderBuilder":
        self.data.setdefault("oralDiet", {})
        return self._push("oralDiet/type", _konsep(nilai, code, display))

    def add_oral_diet_schedule(self, timeline: Any) -> "NutritionOrderBuilder":
        self.data.setdefault("oralDiet", {})
        return self._push("oralDiet/schedule", timeline)

    def add_supplement(self, supplement: Dict[str, Any]) -> "NutritionOrderBuilder":
        return self._push("supplement", supplement)

    def set_enteral_formula(self, formula: Dict[str, Any]) -> "NutritionOrderBuilder":
        self.data["enteralFormula"] = formula
        return self

    # --- alias nama lama ------------------------------------------------------

    def status(self, value: str) -> "NutritionOrderBuilder":
        return self.set_status(value)

    def intent(self, value: str) -> "NutritionOrderBuilder":
        return self.set_intent(value)

    def patient(self, reference: str) -> "NutritionOrderBuilder":
        return self.set_patient(reference)

    def date_time(self, value: str) -> "NutritionOrderBuilder":
        return self.set_date_time(value)

    def orderer(self, reference: str) -> "NutritionOrderBuilder":
        return self.set_orderer(reference)
