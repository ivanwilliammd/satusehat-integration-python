from typing import Optional
from src.builder.base_builder import BaseBuilder


class SearchParameterBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("SearchParameter")

    def set_id(id: str) -> "SearchParameterBuilder":
        self._set("id", id)
        return self

    def add_identifier(system: str, value: str) -> "SearchParameterBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(status: str) -> "SearchParameterBuilder":
        self._set("status", status)
        return self

    def set_code(code: dict) -> "SearchParameterBuilder":
        self._set("code", code)
        return self

    def set_subject(reference: str, display: str = None) -> "SearchParameterBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(description: str) -> "SearchParameterBuilder":
        self._set("description", description)
        return self
