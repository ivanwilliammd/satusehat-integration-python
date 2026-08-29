from typing import Any, Dict, List, Optional

from src.builder.base_builder import BaseBuilder


class ObservationBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Observation")

    def add_identifier(self, system: str, value: str) -> "ObservationBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append({"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "ObservationBuilder":
        self.data["status"] = status
        return self

    def add_category(
        self,
        code: str,
        display: str,
        system: str = "http://terminology.hl7.org/CodeSystem/observation-category",
    ) -> "ObservationBuilder":
        if "category" not in self.data:
            self.data["category"] = []
        self.data["category"].append({
            "coding": [{"system": system, "code": code, "display": display}]
        })
        return self

    def set_code(
        self,
        code: str,
        display: str,
        system: str = "http://loinc.org",
    ) -> "ObservationBuilder":
        self.data["code"] = {
            "coding": [{"system": system, "code": code, "display": display}]
        }
        return self

    def set_subject(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ObservationBuilder":
        subj: Dict[str, Any] = {"reference": reference}
        if display:
            subj["display"] = display
        self.data["subject"] = subj
        return self

    def set_encounter(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ObservationBuilder":
        enc: Dict[str, Any] = {"reference": reference}
        if display:
            enc["display"] = display
        self.data["encounter"] = enc
        return self

    def set_effective_time(self, effective_time: str) -> "ObservationBuilder":
        self.data["effectiveTime"] = effective_time
        return self

    def set_value_quantity(
        self,
        value: float,
        unit: str,
        system: str = "http://unitsofmeasure.org",
        code: str = "",
    ) -> "ObservationBuilder":
        qty: Dict[str, Any] = {"value": value, "unit": unit}
        if code:
            qty["system"] = system
            qty["code"] = code
        self.data["valueQuantity"] = qty
        return self

    def set_value_string(self, value: str) -> "ObservationBuilder":
        self.data["valueString"] = value
        return self

    def set_value_boolean(self, value: bool) -> "ObservationBuilder":
        self.data["valueBoolean"] = value
        return self

    def set_interpretation(
        self,
        code: str,
        display: Optional[str] = None,
    ) -> "ObservationBuilder":
        self.data["interpretation"] = {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                "code": code,
                "display": display,
            }]
        }
        return self

    def add_reference_range(
        self,
        low_value: float,
        low_unit: str,
        high_value: float,
        high_unit: str,
        low_code: Optional[str] = None,
        high_code: Optional[str] = None,
    ) -> "ObservationBuilder":
        if "referenceRange" not in self.data:
            self.data["referenceRange"] = []
        ref: Dict[str, Any] = {
            "low": {"value": low_value, "unit": low_unit},
            "high": {"value": high_value, "unit": high_unit},
        }
        if low_code:
            ref["low"]["code"] = low_code
        if high_code:
            ref["high"]["code"] = high_code
        self.data["referenceRange"].append(ref)
        return self

    def add_performer(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ObservationBuilder":
        if "performer" not in self.data:
            self.data["performer"] = []
        perf: Dict[str, Any] = {"reference": reference}
        if display:
            perf["display"] = display
        self.data["performer"].append(perf)
        return self
