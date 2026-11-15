from typing import Optional
from src.builder.base_builder import BaseBuilder


class BodyStructureBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("BodyStructure")

    def set_id(self, id: str) -> "BodyStructureBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "BodyStructureBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "BodyStructureBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "BodyStructureBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "BodyStructureBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "BodyStructureBuilder":
        self._set("description", description)
        return self

    def set_encounter(self, reference: str) -> "BodyStructureBuilder":
        self._set("encounter", {"reference": reference})
        return self
