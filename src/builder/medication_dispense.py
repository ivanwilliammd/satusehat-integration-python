from typing import Any, Optional

from src.builder.base_builder import BaseBuilder

def _arr(value: Any) -> Any:
    return value.to_array() if hasattr(value, "to_array") else value


def _ref(resource_type: str, nilai: str) -> str:
    """Id polos diberi awalan tipe, seperti Builder::reference() di PHP."""
    if nilai.startswith(("urn:", "http://", "https://")) or "/" in nilai:
        return nilai
    return f"{resource_type}/{nilai}"


class MedicationDispenseBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("MedicationDispense")

    def status(self, value: str) -> "MedicationDispenseBuilder":
        return self._set("status", value)

    def medication(self, codeable_concept: dict) -> "MedicationDispenseBuilder":
        return self._set("medication", codeable_concept)

    def subject(self, reference: str) -> "MedicationDispenseBuilder":
        return self._set("subject", {"reference": reference})

    def encounter(self, reference: str) -> "MedicationDispenseBuilder":
        return self._set("encounter", {"reference": reference})

    def when_prepared(self, value: str) -> "MedicationDispenseBuilder":
        return self._set("whenPrepared", value)

    def when_handed_over(self, value: str) -> "MedicationDispenseBuilder":
        return self._set("whenHandedOver", value)

    def destination(self, reference: str) -> "MedicationDispenseBuilder":
        return self._set("destination", {"reference": reference})

    # --- Nama kanon (cermin PayloadBuilderMedicationDispense) ---

    def set_id(self, id: str) -> "MedicationDispenseBuilder":
        return self._set("id", id)

    def add_identifier(self, system: str, value: str) -> "MedicationDispenseBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_medication_reference(self, reference: str, display: Optional[str] = None) -> "MedicationDispenseBuilder":
        ref: dict = {"reference": reference}
        if display is not None:
            ref["display"] = display
        return self._set("medicationReference", ref)

    def set_subject(self, subject_id: str, display: Optional[str] = None) -> "MedicationDispenseBuilder":
        ref: dict = {"reference": _ref("Patient", subject_id)}
        if display is not None:
            ref["display"] = display
        return self._set("subject", ref)

    def set_context(self, context_id: str) -> "MedicationDispenseBuilder":
        self.data.setdefault("context", {})["reference"] = _ref("Encounter", context_id)
        return self

    def add_performer(self, actor_id: str, display: Optional[str] = None) -> "MedicationDispenseBuilder":
        actor: dict = {"reference": _ref("Practitioner", actor_id)}
        if display is not None:
            actor["display"] = display
        return self._push("performer", {"actor": actor})

    def set_location(self, location_id: str, display: Optional[str] = None) -> "MedicationDispenseBuilder":
        ref: dict = {"reference": _ref("Location", location_id)}
        if display is not None:
            ref["display"] = display
        return self._set("location", ref)

    def add_authorizing_prescription(self, request_id: str) -> "MedicationDispenseBuilder":
        return self._push("authorizingPrescription", {"reference": _ref("MedicationRequest", request_id)})

    def set_category(self, code: str, display: Optional[str] = None,
                     system: str = "http://terminology.hl7.org/CodeSystem/medicationdispense-category") -> "MedicationDispenseBuilder":
        coding: dict = {"system": system, "code": code}
        if display is not None:
            coding["display"] = display
        self.data.setdefault("category", {})["coding"] = [coding]
        return self

    def set_quantity(self, value: float, unit: str, system: Optional[str] = None,
                     code: Optional[str] = None) -> "MedicationDispenseBuilder":
        quantity: dict = {"value": value, "unit": unit}
        if system is not None:
            quantity["system"] = system
        if code is not None:
            quantity["code"] = code
        return self._set("quantity", quantity)

    def set_days_supply(self, value: float, unit: str, system: Optional[str] = None,
                        code: Optional[str] = None) -> "MedicationDispenseBuilder":
        days: dict = {"value": value, "unit": unit}
        if system is not None:
            days["system"] = system
        if code is not None:
            days["code"] = code
        return self._set("daysSupply", days)

    def add_dosage_instruction(self, sequence: int, text: str, dose_value: float, dose_unit: str,
                               route_code: str, route_display: str, timing_code: str, timing_display: str,
                               additional_code: str, additional_text: str) -> "MedicationDispenseBuilder":
        return self._push("dosageInstruction", {
            "sequence": sequence,
            "text": text,
            "additionalInstruction": [{"coding": [{"code": additional_code, "display": additional_text}]}],
            "timing": {"code": {"coding": [{"code": timing_code, "display": timing_display}]}},
            "route": {"coding": [{"code": route_code, "display": route_display}]},
            "doseAndRate": [{"doseQuantity": {"value": dose_value, "unit": dose_unit}}],
        })

    def set_substitution(self, was_substituted: bool, type_code: Optional[str] = None,
                         type_display: Optional[str] = None) -> "MedicationDispenseBuilder":
        substitution: dict = {"wasSubstituted": was_substituted}
        if type_code is not None:
            coding: dict = {"code": type_code}
            if type_display is not None:
                coding["display"] = type_display
            substitution["type"] = {"coding": [coding]}
        return self._set("substitution", substitution)

    def add_contained(self, resource: dict) -> "MedicationDispenseBuilder":
        return self._push("contained", resource)
