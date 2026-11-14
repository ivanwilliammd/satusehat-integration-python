from typing import Optional
from src.builder.base_builder import BaseBuilder


class ResearchDefinitionBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ResearchDefinition")

    def set_id(self, id: str) -> "ResearchDefinitionBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "ResearchDefinitionBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "ResearchDefinitionBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "ResearchDefinitionBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "ResearchDefinitionBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "ResearchDefinitionBuilder":
        self._set("description", description)
        return self
