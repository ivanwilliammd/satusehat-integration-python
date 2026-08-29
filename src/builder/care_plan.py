"""CarePlan resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from .base import BaseBuilder


class CarePlanBuilder(BaseBuilder):
    """Builder for CarePlan resource."""

    def __init__(self):
        super().__init__()
        self._data = {"resourceType": "CarePlan"}

    def set_id(self, id: str) -> "CarePlanBuilder":
        self._data["id"] = id
        return self

    def set_status(self, status: str) -> "CarePlanBuilder":
        self._data["status"] = status
        return self

    def set_intent(self, intent: str) -> "CarePlanBuilder":
        self._data["intent"] = intent
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "CarePlanBuilder":
        self._data["subject"] = {"reference": reference}
        if display:
            self._data["subject"]["display"] = display
        return self

    def set_encounter(self, reference: str) -> "CarePlanBuilder":
        self._data["encounter"] = {"reference": reference}
        return self

    def set_period(self, start: Optional[str] = None, end: Optional[str] = None) -> "CarePlanBuilder":
        period: dict = {}
        if start:
            period["start"] = start
        if end:
            period["end"] = end
        self._data["period"] = period
        return self

    def set_author(self, reference: str, display: Optional[str] = None) -> "CarePlanBuilder":
        self._data["author"] = {"reference": reference}
        if display:
            self._data["author"]["display"] = display
        return self

    def add_category(self, code: str, system: str, display: Optional[str] = None) -> "CarePlanBuilder":
        self._data.setdefault("category", [])
        cat: dict = {"coding": [{"system": system, "code": code}]}
        if display:
            cat["coding"][0]["display"] = display
        self._data["category"].append(cat)
        return self

    def add_addresses(self, reference: str, display: Optional[str] = None) -> "CarePlanBuilder":
        self._data.setdefault("addresses", [])
        addr: dict = {"reference": reference}
        if display:
            addr["display"] = display
        self._data["addresses"].append(addr)
        return self

    def add_supporting_info(self, reference: str) -> "CarePlanBuilder":
        self._data.setdefault("supportingInfo", [])
        self._data["supportingInfo"].append({"reference": reference})
        return self

    def add_activity(
        self,
        detail_code: Optional[str] = None,
        detail_system: Optional[str] = None,
        detail_display: Optional[str] = None,
        status: Optional[str] = None
    ) -> "CarePlanBuilder":
        self._data.setdefault("activity", [])
        activity: dict = {}
        if detail_code:
            activity["detail"] = {"code": {"coding": [{"code": detail_code}]}}
            if detail_system:
                activity["detail"]["code"]["coding"][0]["system"] = detail_system
            if detail_display:
                activity["detail"]["code"]["coding"][0]["display"] = detail_display
        if status:
            activity.setdefault("detail", {})["status"] = status
        self._data["activity"].append(activity)
        return self

    def add_note(self, text: str) -> "CarePlanBuilder":
        self._data.setdefault("note", [])
        self._data["note"].append({"text": text})
        return self
