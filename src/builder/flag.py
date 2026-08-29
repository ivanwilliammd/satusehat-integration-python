from typing import Optional
from src.builder.base_builder import BaseBuilder


class FlagBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("Flag")

    def set_id(id: str) -> "FlagBuilder":
        self._set("id", id)
        return self

    def add_identifier(system: str, value: str) -> "FlagBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(status: str) -> "FlagBuilder":
        self._set("status", status)
        return self

    def set_code(code: dict) -> "FlagBuilder":
        self._set("code", code)
        return self

    def set_subject(reference: str, display: str = None) -> "FlagBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(description: str) -> "FlagBuilder":
        self._set("description", description)
        return self
