from typing import Optional
from src.builder.base_builder import BaseBuilder


class ResearchSubjectBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ResearchSubject")

    def set_id(self, id: str) -> "ResearchSubjectBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "ResearchSubjectBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "ResearchSubjectBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "ResearchSubjectBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "ResearchSubjectBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "ResearchSubjectBuilder":
        self._set("description", description)
        return self

    def set_encounter(self, reference: str) -> "ResearchSubjectBuilder":
        self._set("encounter", {"reference": reference})
        return self
