"""ChargeItem resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class ChargeItemBuilder(BaseBuilder):
    """Builder for ChargeItem resource."""

    def __init__(self):
        super().__init__("ChargeItemBuilder")
        self.data = {"resourceType": "ChargeItem"}

    def set_id(self, id: str) -> "ChargeItemBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "ChargeItemBuilder":
        self.data["status"] = status
        return self

    def set_code(self, code: str, system: str, display: Optional[str] = None) -> "ChargeItemBuilder":
        self.data["code"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["code"]["coding"][0]["display"] = display
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "ChargeItemBuilder":
        self.data["subject"] = {"reference": reference}
        if display:
            self.data["subject"]["display"] = display
        return self

    def set_encounter(self, reference: str) -> "ChargeItemBuilder":
        self.data["encounter"] = {"reference": reference}
        return self

    def set_occurence_datetime(self, occurence_datetime: str) -> "ChargeItemBuilder":
        self.data["occurrenceDateTime"] = occurence_datetime
        return self

    def set_performer(self, function_code: str, function_system: str, actor_reference: str, actor_display: Optional[str] = None) -> "ChargeItemBuilder":
        self.data.setdefault("performer", [])
        perf: dict = {
            "function": {"coding": [{"code": function_code, "system": function_system}]},
            "actor": {"reference": actor_reference}
        }
        if actor_display:
            perf["actor"]["display"] = actor_display
        self.data["performer"].append(perf)
        return self

    def set_performing_organization(self, reference: str, display: Optional[str] = None) -> "ChargeItemBuilder":
        self.data["performingOrganization"] = {"reference": reference}
        if display:
            self.data["performingOrganization"]["display"] = display
        return self

    def set_requesting_organization(self, reference: str, display: Optional[str] = None) -> "ChargeItemBuilder":
        self.data["requestingOrganization"] = {"reference": reference}
        if display:
            self.data["requestingOrganization"]["display"] = display
        return self

    def set_quantity(self, value: float, code: str, system: str) -> "ChargeItemBuilder":
        self.data["quantity"] = {"value": value, "code": code, "system": system}
        return self

    def set_bodysite(self, code: str, system: str, display: Optional[str] = None) -> "ChargeItemBuilder":
        self.data["bodySite"] = [{"coding": [{"system": system, "code": code}]}]
        if display:
            self.data["bodySite"][0]["coding"][0]["display"] = display
        return self

    def add_factor_override(self, factor: float) -> "ChargeItemBuilder":
        self.data["factorOverride"] = factor
        return self

    def add_reason(self, code: str, system: str, display: Optional[str] = None) -> "ChargeItemBuilder":
        self.data.setdefault("reason", [])
        reason: dict = {"coding": [{"system": system, "code": code}]}
        if display:
            reason["coding"][0]["display"] = display
        self.data["reason"].append(reason)
        return self

    def add_service(self, reference: str) -> "ChargeItemBuilder":
        self.data.setdefault("service", [])
        self.data["service"].append({"reference": reference})
        return self
