"""Account resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class AccountBuilder(BaseBuilder):
    """Builder for Account resource."""

    def __init__(self):
        super().__init__("AccountBuilder")
        self.data = {"resourceType": "Account"}

    def set_id(self, id: str) -> "AccountBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "AccountBuilder":
        self.data["status"] = status
        return self

    def set_type(self, code: str, system: str, display: Optional[str] = None) -> "AccountBuilder":
        self.data["type"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["type"]["coding"][0]["display"] = display
        return self

    def set_name(self, name: str) -> "AccountBuilder":
        self.data["name"] = name
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "AccountBuilder":
        self.data["subject"] = {"reference": reference}
        if display:
            self.data["subject"]["display"] = display
        return self

    def set_service_period(self, start: Optional[str] = None, end: Optional[str] = None) -> "AccountBuilder":
        period: dict = {}
        if start:
            period["start"] = start
        if end:
            period["end"] = end
        self.data["servicePeriod"] = period
        return self

    def add_coverage(
        self,
        coverage_reference: str,
        priority: Optional[int] = None,
        coverage_display: Optional[str] = None
    ) -> "AccountBuilder":
        self.data.setdefault("coverage", [])
        cov: dict = {"coverage": {"reference": coverage_reference}}
        if priority:
            cov["priority"] = priority
        if coverage_display:
            cov["coverage"]["display"] = coverage_display
        self.data["coverage"].append(cov)
        return self

    def set_owner(self, reference: str, display: Optional[str] = None) -> "AccountBuilder":
        self.data["owner"] = {"reference": reference}
        if display:
            self.data["owner"]["display"] = display
        return self

    def set_description(self, description: str) -> "AccountBuilder":
        self.data["description"] = description
        return self
