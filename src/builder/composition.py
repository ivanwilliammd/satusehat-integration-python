"""Composition resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class CompositionBuilder(BaseBuilder):
    """Builder for Composition resource."""

    def __init__(self):
        super().__init__("CompositionBuilder")
        self.data = {"resourceType": "Composition"}

    def set_id(self, id: str) -> "CompositionBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "CompositionBuilder":
        self.data["status"] = status
        return self

    def set_type(self, code: str, system: str, display: Optional[str] = None) -> "CompositionBuilder":
        self.data["type"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["type"]["coding"][0]["display"] = display
        return self

    def set_category(self, code: str, system: str, display: Optional[str] = None) -> "CompositionBuilder":
        self.data["category"] = [{"coding": [{"system": system, "code": code}]}]
        if display:
            self.data["category"][0]["coding"][0]["display"] = display
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "CompositionBuilder":
        self.data["subject"] = {"reference": reference}
        if display:
            self.data["subject"]["display"] = display
        return self

    def set_encounter(self, reference: str) -> "CompositionBuilder":
        self.data["encounter"] = {"reference": reference}
        return self

    def set_date(self, date: str) -> "CompositionBuilder":
        self.data["date"] = date
        return self

    def set_author(self, reference: str, display: Optional[str] = None) -> "CompositionBuilder":
        self.data["author"] = [{"reference": reference}]
        if display:
            self.data["author"][0]["display"] = display
        return self

    def set_title(self, title: str) -> "CompositionBuilder":
        self.data["title"] = title
        return self

    def set_confidentiality(self, confidentiality: str) -> "CompositionBuilder":
        self.data["confidentiality"] = confidentiality
        return self

    def add_section(
        self,
        title: Optional[str] = None,
        code: Optional[str] = None,
        code_system: Optional[str] = None,
        code_display: Optional[str] = None
    ) -> "CompositionBuilder":
        self.data.setdefault("section", [])
        section: dict = {}
        if title:
            section["title"] = title
        if code:
            section["code"] = {"coding": [{"code": code}]}
            if code_system:
                section["code"]["coding"][0]["system"] = code_system
            if code_display:
                section["code"]["coding"][0]["display"] = code_display
        self.data["section"].append(section)
        return self

    def add_section_entry(self, index: int, reference: str) -> "CompositionBuilder":
        if "section" in self.data and len(self.data["section"]) > index:
            self.data["section"][index].setdefault("entry", [])
            self.data["section"][index]["entry"].append({"reference": reference})
        return self
