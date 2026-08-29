"""Composition resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from .base import BaseBuilder


class CompositionBuilder(BaseBuilder):
    """Builder for Composition resource."""

    def __init__(self):
        super().__init__()
        self._data = {"resourceType": "Composition"}

    def set_id(self, id: str) -> "CompositionBuilder":
        self._data["id"] = id
        return self

    def set_status(self, status: str) -> "CompositionBuilder":
        self._data["status"] = status
        return self

    def set_type(self, code: str, system: str, display: Optional[str] = None) -> "CompositionBuilder":
        self._data["type"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self._data["type"]["coding"][0]["display"] = display
        return self

    def set_category(self, code: str, system: str, display: Optional[str] = None) -> "CompositionBuilder":
        self._data["category"] = [{"coding": [{"system": system, "code": code}]}]
        if display:
            self._data["category"][0]["coding"][0]["display"] = display
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "CompositionBuilder":
        self._data["subject"] = {"reference": reference}
        if display:
            self._data["subject"]["display"] = display
        return self

    def set_encounter(self, reference: str) -> "CompositionBuilder":
        self._data["encounter"] = {"reference": reference}
        return self

    def set_date(self, date: str) -> "CompositionBuilder":
        self._data["date"] = date
        return self

    def set_author(self, reference: str, display: Optional[str] = None) -> "CompositionBuilder":
        self._data["author"] = [{"reference": reference}]
        if display:
            self._data["author"][0]["display"] = display
        return self

    def set_title(self, title: str) -> "CompositionBuilder":
        self._data["title"] = title
        return self

    def set_confidentiality(self, confidentiality: str) -> "CompositionBuilder":
        self._data["confidentiality"] = confidentiality
        return self

    def add_section(
        self,
        title: Optional[str] = None,
        code: Optional[str] = None,
        code_system: Optional[str] = None,
        code_display: Optional[str] = None
    ) -> "CompositionBuilder":
        self._data.setdefault("section", [])
        section: dict = {}
        if title:
            section["title"] = title
        if code:
            section["code"] = {"coding": [{"code": code}]}
            if code_system:
                section["code"]["coding"][0]["system"] = code_system
            if code_display:
                section["code"]["coding"][0]["display"] = code_display
        self._data["section"].append(section)
        return self

    def add_section_entry(self, index: int, reference: str) -> "CompositionBuilder":
        if "section" in self._data and len(self._data["section"]) > index:
            self._data["section"][index].setdefault("entry", [])
            self._data["section"][index]["entry"].append({"reference": reference})
        return self
