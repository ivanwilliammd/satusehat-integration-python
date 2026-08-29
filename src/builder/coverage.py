"""Coverage resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from .base import BaseBuilder


class CoverageBuilder(BaseBuilder):
    """Builder for Coverage resource."""

    def __init__(self):
        super().__init__()
        self._data = {"resourceType": "Coverage"}

    def set_id(self, id: str) -> "CoverageBuilder":
        self._data["id"] = id
        return self

    def set_status(self, status: str) -> "CoverageBuilder":
        self._data["status"] = status
        return self

    def set_policy_holder(self, reference: str, display: Optional[str] = None) -> "CoverageBuilder":
        self._data["policyHolder"] = {"reference": reference}
        if display:
            self._data["policyHolder"]["display"] = display
        return self

    def set_subscriber(self, reference: str, display: Optional[str] = None) -> "CoverageBuilder":
        self._data["subscriber"] = {"reference": reference}
        if display:
            self._data["subscriber"]["display"] = display
        return self

    def set_subscriber_id(self, subscriber_id: str) -> "CoverageBuilder":
        self._data["subscriberId"] = subscriber_id
        return self

    def set_beneficiary(self, reference: str, display: Optional[str] = None) -> "CoverageBuilder":
        self._data["beneficiary"] = {"reference": reference}
        if display:
            self._data["beneficiary"]["display"] = display
        return self

    def set_dependent(self, dependent: str) -> "CoverageBuilder":
        self._data["dependent"] = dependent
        return self

    def set_relationship(self, code: str, system: str, display: Optional[str] = None) -> "CoverageBuilder":
        self._data["relationship"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self._data["relationship"]["coding"][0]["display"] = display
        return self

    def set_period(self, start: Optional[str] = None, end: Optional[str] = None) -> "CoverageBuilder":
        period: dict = {}
        if start:
            period["start"] = start
        if end:
            period["end"] = end
        self._data["period"] = period
        return self

    def add_payor(self, reference: str, display: Optional[str] = None) -> "CoverageBuilder":
        self._data.setdefault("payor", [])
        payor: dict = {"reference": reference}
        if display:
            payor["display"] = display
        self._data["payor"].append(payor)
        return self

    def set_class(
        self,
        type_code: str,
        type_system: str,
        value: str,
        name: Optional[str] = None
    ) -> "CoverageBuilder":
        cls: dict = {"type": {"coding": [{"system": type_system, "code": type_code}]}, "value": value}
        if name:
            cls["name"] = name
        self._data["class"] = [cls]
        return self

    def set_network(self, network: str) -> "CoverageBuilder":
        self._data["network"] = network
        return self

    def add_cost_to_beneficiary(
        self,
        type_code: str,
        type_system: str,
        value: float,
        code: Optional[str] = None,
        code_system: Optional[str] = None
    ) -> "CoverageBuilder":
        self._data.setdefault("costToBeneficiary", [])
        ctb: dict = {
            "type": {"coding": [{"system": type_system, "code": type_code}]},
            "valueQuantity": {"value": value}
        }
        if code:
            ctb["valueQuantity"]["code"] = code
        if code_system:
            ctb["valueQuantity"]["system"] = code_system
        self._data["costToBeneficiary"].append(ctb)
        return self
