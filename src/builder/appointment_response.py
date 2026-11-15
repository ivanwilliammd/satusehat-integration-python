from typing import Optional
from src.builder.base_builder import BaseBuilder


class AppointmentResponseBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("AppointmentResponse")

    def set_id(self, id: str) -> "AppointmentResponseBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "AppointmentResponseBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "AppointmentResponseBuilder":
        self._set("status", status)
        return self

    def set_code(self, system, code: str = "", display: str = "") -> "AppointmentResponseBuilder":
        """Menerima (system, code, display) seperti PHP, atau satu dict CodeableConcept."""
        if isinstance(system, dict):
            self._set("code", system)
            return self
        konsep = {"coding": [{"system": system, "code": code}]}
        if display:
            konsep["coding"][0]["display"] = display
        self._set("code", konsep)
        return self

    def set_subject(self, reference: str, display: str = None) -> "AppointmentResponseBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "AppointmentResponseBuilder":
        self._set("description", description)
        return self

    def set_encounter(self, reference: str) -> "AppointmentResponseBuilder":
        return self._set("encounter", {"reference": reference})
