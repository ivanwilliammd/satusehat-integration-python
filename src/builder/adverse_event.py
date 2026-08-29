from typing import Optional
from src.builder.base_builder import BaseBuilder


class AdverseEventBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("AdverseEvent")

    def set_id(id: str) -> "AdverseEventBuilder":
        self._set("id", id)
        return self

    def add_identifier(system: str, value: str) -> "AdverseEventBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(status: str) -> "AdverseEventBuilder":
        self._set("status", status)
        return self

    def set_code(code: dict) -> "AdverseEventBuilder":
        self._set("code", code)
        return self

    def set_subject(reference: str, display: str = None) -> "AdverseEventBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(description: str) -> "AdverseEventBuilder":
        self._set("description", description)
        return self
