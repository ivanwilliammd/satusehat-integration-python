from .base_builder import BaseBuilder
from ..datatype.datatypes import CodeableConcept, Reference

class ListResourceBuilder(BaseBuilder):
    resourceType = "List"

    def __init__(self):
        super().__init__(self.resourceType)

    def set_id(self, id: str) -> "ListResourceBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "ListResourceBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "ListResourceBuilder":
        self._set("status", status)
        return self

    def set_mode(self, mode: str) -> "ListResourceBuilder":
        self._set("mode", mode)
        return self

    def set_code(self, code: CodeableConcept) -> "ListResourceBuilder":
        self._set("code", code.to_array())
        return self

    def set_subject(self, ref: Reference) -> "ListResourceBuilder":
        self._set("subject", ref.to_array())
        return self

    def set_date(self, date: str) -> "ListResourceBuilder":
        self._set("date", date)
        return self

    def set_title(self, title: str) -> "ListResourceBuilder":
        self._set("title", title)
        return self
