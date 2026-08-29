"""List resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from .base import BaseBuilder


class ListResourceBuilder(BaseBuilder):
    """Builder for List resource."""

    def __init__(self):
        super().__init__()
        self._data = {"resourceType": "List"}

    def set_id(self, id: str) -> "ListResourceBuilder":
        self._data["id"] = id
        return self

    def set_status(self, status: str) -> "ListResourceBuilder":
        self._data["status"] = status
        return self

    def set_mode(self, mode: str) -> "ListResourceBuilder":
        self._data["mode"] = mode
        return self

    def set_title(self, title: str) -> "ListResourceBuilder":
        self._data["title"] = title
        return self

    def set_code(self, code: str, system: str, display: Optional[str] = None) -> "ListResourceBuilder":
        self._data["code"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self._data["code"]["coding"][0]["display"] = display
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "ListResourceBuilder":
        self._data["subject"] = {"reference": reference}
        if display:
            self._data["subject"]["display"] = display
        return self

    def set_encounter(self, reference: str) -> "ListResourceBuilder":
        self._data["encounter"] = {"reference": reference}
        return self

    def set_date(self, date: str) -> "ListResourceBuilder":
        self._data["date"] = date
        return self

    def set_source(self, reference: str, display: Optional[str] = None) -> "ListResourceBuilder":
        self._data["source"] = {"reference": reference}
        if display:
            self._data["source"]["display"] = display
        return self

    def set_ordered_by(self, code: str, system: str, display: Optional[str] = None) -> "ListResourceBuilder":
        self._data["orderedBy"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self._data["orderedBy"]["coding"][0]["display"] = display
        return self

    def add_entry(
        self,
        reference: str,
        flag_code: Optional[str] = None,
        flag_system: Optional[str] = None,
        flag_display: Optional[str] = None,
        deleted: bool = False
    ) -> "ListResourceBuilder":
        self._data.setdefault("entry", [])
        entry: dict = {"item": {"reference": reference}}
        if deleted:
            entry["deleted"] = True
        if flag_code:
            entry["flag"] = {"coding": [{"code": flag_code}]}
            if flag_system:
                entry["flag"]["coding"][0]["system"] = flag_system
            if flag_display:
                entry["flag"]["coding"][0]["display"] = flag_display
        self._data["entry"].append(entry)
        return self

    def add_note(self, text: str) -> "ListResourceBuilder":
        self._data.setdefault("note", [])
        self._data["note"].append({"text": text})
        return self
