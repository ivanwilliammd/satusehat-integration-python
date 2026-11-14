from typing import Optional
from src.builder.base_builder import BaseBuilder


class FlagBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("Flag")

    def set_id(self, id: str) -> "FlagBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "FlagBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "FlagBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "FlagBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "FlagBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "FlagBuilder":
        self._set("description", description)
        return self
