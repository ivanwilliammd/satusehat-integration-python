"""Account resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from .base import BaseBuilder


class AccountBuilder(BaseBuilder):
    """Builder for Account resource."""

    def __init__(self):
        super().__init__()
        self._data = {"resourceType": "Account"}

    def set_id(self, id: str) -> "AccountBuilder":
        self._data["id"] = id
        return self

    def set_status(self, status: str) -> "AccountBuilder":
        self._data["status"] = status
        return self

    def set_type(self, code: str, system: str, display: Optional[str] = None) -> "AccountBuilder":
        self._data["type"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self._data["type"]["coding"][0]["display"] = display
        return self

    def set_name(self, name: str) -> "AccountBuilder":
        self._data["name"] = name
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "AccountBuilder":
        self._data["subject"] = {"reference": reference}
        if display:
            self._data["subject"]["display"] = display
        return self

    def set_service_period(self, start: Optional[str] = None, end: Optional[str] = None) -> "AccountBuilder":
        period: dict = {}
        if start:
            period["start"] = start
        if end:
            period["end"] = end
        self._data["servicePeriod"] = period
        return self

    def add_coverage(
        self,
        coverage_reference: str,
        priority: Optional[int] = None,
        coverage_display: Optional[str] = None
    ) -> "AccountBuilder":
        self._data.setdefault("coverage", [])
        cov: dict = {"coverage": {"reference": coverage_reference}}
        if priority:
            cov["priority"] = priority
        if coverage_display:
            cov["coverage"]["display"] = coverage_display
        self._data["coverage"].append(cov)
        return self

    def set_owner(self, reference: str, display: Optional[str] = None) -> "AccountBuilder":
        self._data["owner"] = {"reference": reference}
        if display:
            self._data["owner"]["display"] = display
        return self

    def set_description(self, description: str) -> "AccountBuilder":
        self._data["description"] = description
        return self
