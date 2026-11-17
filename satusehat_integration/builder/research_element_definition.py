from typing import Optional
from satusehat_integration.builder.base_builder import BaseBuilder


class ResearchElementDefinitionBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ResearchElementDefinition")

    def set_id(self, id: str) -> "ResearchElementDefinitionBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "ResearchElementDefinitionBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "ResearchElementDefinitionBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "ResearchElementDefinitionBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "ResearchElementDefinitionBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "ResearchElementDefinitionBuilder":
        self._set("description", description)
        return self

    def set_encounter(self, reference: str) -> "ResearchElementDefinitionBuilder":
        self._set("encounter", {"reference": reference})
        return self
