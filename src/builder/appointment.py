from typing import Optional
from src.builder.base_builder import BaseBuilder


class AppointmentBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("Appointment")

    def set_id(self, id: str) -> "AppointmentBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "AppointmentBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "AppointmentBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "AppointmentBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "AppointmentBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "AppointmentBuilder":
        self._set("description", description)
        return self
