from typing import Optional
from src.builder.base_builder import BaseBuilder


class SearchParameterBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("SearchParameter")

    def set_id(self, id: str) -> "SearchParameterBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "SearchParameterBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "SearchParameterBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "SearchParameterBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "SearchParameterBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "SearchParameterBuilder":
        self._set("description", description)
        return self
