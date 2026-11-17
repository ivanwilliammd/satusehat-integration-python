from typing import Optional
from satusehat_integration.builder.base_builder import BaseBuilder


class EventDefinitionBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("EventDefinition")

    def set_id(self, id: str) -> "EventDefinitionBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "EventDefinitionBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "EventDefinitionBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "EventDefinitionBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "EventDefinitionBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "EventDefinitionBuilder":
        self._set("description", description)
        return self

    def set_encounter(self, reference: str) -> "EventDefinitionBuilder":
        self._set("encounter", {"reference": reference})
        return self
