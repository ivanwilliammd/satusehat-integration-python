from typing import Any, Optional
from src.builder.base_builder import BaseBuilder


class MedicationStatementBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("MedicationStatement")

    def set_id(self, val: str) -> "MedicationStatementBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str) -> "MedicationStatementBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_status(self, val: str) -> "MedicationStatementBuilder":
        return self._set("status", val)

    def add_status_reason(self, code: str, display: str = None, system: str = None) -> "MedicationStatementBuilder":
        coding = {"code": code, "display": display if display else code}
        if system:
            coding["system"] = system
        return self._push("statusReason", {"coding": [coding]})

    def set_medication_codeable_concept(self, cc: dict) -> "MedicationStatementBuilder":
        return self._set("medicationCodeableConcept", cc)

    def set_medication_reference(self, ref: str, display: str = None) -> "MedicationStatementBuilder":
        return self._set("medicationReference", self._ref(ref, "Medication", display))

    def set_subject(self, ref: str, display: str = None) -> "MedicationStatementBuilder":
        return self._set("subject", self._ref(ref, "Patient", display))

    def set_context(self, ref: str, display: str = None) -> "MedicationStatementBuilder":
        return self._set("context", self._ref(ref, "Encounter", display))

    def set_date_asserted(self, val: str) -> "MedicationStatementBuilder":
        return self._set("dateAsserted", val)

    def set_effective_date_time(self, val: str) -> "MedicationStatementBuilder":
        return self._set("effectiveDateTime", val)

    def set_information_source(self, ref: str, display: str = None) -> "MedicationStatementBuilder":
        return self._set("informationSource", self._ref(ref, "Patient", display))

    def set_derived_from(self, ref: str) -> "MedicationStatementBuilder":
        return self._push("derivedFrom", {"reference": ref})

    def add_reason_code(self, cc: dict) -> "MedicationStatementBuilder":
        return self._push("reasonCode", cc)

    def add_reason_reference(self, ref: str) -> "MedicationStatementBuilder":
        return self._push("reasonReference", {"reference": ref})

    def add_note(self, text: str) -> "MedicationStatementBuilder":
        return self._push("note", {"text": text})

    def add_contained(self, resource: dict) -> "MedicationStatementBuilder":
        return self._push("contained", resource)

    def add_dosage_instruction(self, text: str = None, frequency: int = None, period: int = None, period_unit: str = None) -> "MedicationStatementBuilder":
        dosage: dict = {}
        if text:
            dosage["text"] = text
        if frequency is not None:
            dosage["sequence"] = frequency
            dosage["timing"] = {"repeat": {"frequency": frequency}}
        if period is not None:
            dosage.setdefault("timing", {"repeat": {}})["repeat"]["period"] = period
        if period_unit:
            dosage.setdefault("timing", {"repeat": {}})["repeat"]["periodUnit"] = period_unit
        return self._push("dosage", dosage)

    def set_category(self, category: Any) -> "MedicationStatementBuilder":
        return self._set("category", category.to_array() if hasattr(category, "to_array") else category)

    def set_effective_period(self, period: Any) -> "MedicationStatementBuilder":
        return self._set("effectivePeriod", period.to_array() if hasattr(period, "to_array") else period)

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "MedicationStatementBuilder":
        extension: dict = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        return self._push("extension", extension)

    def set_reason_code(self, konsep) -> "MedicationStatementBuilder":
        return self.add_reason_code(konsep)

    def set_reason_reference(self, reference) -> "MedicationStatementBuilder":
        return self.add_reason_reference(reference)
