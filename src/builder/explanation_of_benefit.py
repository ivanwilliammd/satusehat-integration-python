"""ExplanationOfBenefit resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from .base import BaseBuilder


class ExplanationOfBenefitBuilder(BaseBuilder):
    """Builder for ExplanationOfBenefit resource."""

    def __init__(self):
        super().__init__()
        self._data = {"resourceType": "ExplanationOfBenefit"}

    def set_id(self, id: str) -> "ExplanationOfBenefitBuilder":
        self._data["id"] = id
        return self

    def set_status(self, status: str) -> "ExplanationOfBenefitBuilder":
        self._data["status"] = status
        return self

    def set_type(self, code: str, system: str, display: Optional[str] = None) -> "ExplanationOfBenefitBuilder":
        self._data["type"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self._data["type"]["coding"][0]["display"] = display
        return self

    def set_sub_type(self, code: str, system: str, display: Optional[str] = None) -> "ExplanationOfBenefitBuilder":
        self._data["subType"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self._data["subType"]["coding"][0]["display"] = display
        return self

    def set_use(self, use: str) -> "ExplanationOfBenefitBuilder":
        self._data["use"] = use
        return self

    def set_patient(self, reference: str, display: Optional[str] = None) -> "ExplanationOfBenefitBuilder":
        self._data["patient"] = {"reference": reference}
        if display:
            self._data["patient"]["display"] = display
        return self

    def set_billable_period(self, start: Optional[str] = None, end: Optional[str] = None) -> "ExplanationOfBenefitBuilder":
        period: dict = {}
        if start:
            period["start"] = start
        if end:
            period["end"] = end
        self._data["billablePeriod"] = period
        return self

    def set_created(self, created: str) -> "ExplanationOfBenefitBuilder":
        self._data["created"] = created
        return self

    def set_insurer(self, reference: str, display: Optional[str] = None) -> "ExplanationOfBenefitBuilder":
        self._data["insurer"] = {"reference": reference}
        if display:
            self._data["insurer"]["display"] = display
        return self

    def set_provider(self, reference: str, display: Optional[str] = None) -> "ExplanationOfBenefitBuilder":
        self._data["provider"] = {"reference": reference}
        if display:
            self._data["provider"]["display"] = display
        return self

    def set_request(self, reference: str) -> "ExplanationOfBenefitBuilder":
        self._data["request"] = {"reference": reference}
        return self

    def add_diagnosis(
        self,
        sequence: int,
        diagnosis_code: str,
        diagnosis_system: str,
        type_code: Optional[str] = None
    ) -> "ExplanationOfBenefitBuilder":
        self._data.setdefault("diagnosis", [])
        diag: dict = {
            "sequence": sequence,
            "diagnosisCodeableConcept": {"coding": [{"code": diagnosis_code, "system": diagnosis_system}]}
        }
        if type_code:
            diag["type"] = [{"coding": [{"code": type_code}]}]
        self._data["diagnosis"].append(diag)
        return self

    def add_insurance(
        self,
        focal: bool,
        coverage_reference: str,
        coverage_display: Optional[str] = None
    ) -> "ExplanationOfBenefitBuilder":
        self._data.setdefault("insurance", [])
        ins: dict = {"focal": focal, "coverage": {"reference": coverage_reference}}
        if coverage_display:
            ins["coverage"]["display"] = coverage_display
        self._data["insurance"].append(ins)
        return self

    def add_item(
        self,
        sequence: int,
        service_code: str,
        service_system: str
    ) -> "ExplanationOfBenefitBuilder":
        self._data.setdefault("item", [])
        item: dict = {
            "sequence": sequence,
            "service": {"coding": [{"code": service_code, "system": service_system}]}
        }
        self._data["item"].append(item)
        return self

    def add_item_encounter(self, item_index: int, encounter_reference: str) -> "ExplanationOfBenefitBuilder":
        if "item" in self._data and len(self._data["item"]) > item_index:
            self._data["item"][item_index].setdefault("encounter", [])
            self._data["item"][item_index]["encounter"].append({"reference": encounter_reference})
        return self

    def add_item_adjudication(
        self,
        item_index: int,
        category_code: str,
        category_system: str,
        value: Optional[float] = None,
        display: Optional[str] = None
    ) -> "ExplanationOfBenefitBuilder":
        if "item" in self._data and len(self._data["item"]) > item_index:
            self._data["item"][item_index].setdefault("adjudication", [])
            adj: dict = {"category": {"coding": [{"code": category_code, "system": category_system}]}}
            if value is not None:
                adj["value"] = value
            if display:
                adj["category"]["coding"][0]["display"] = display
            self._data["item"][item_index]["adjudication"].append(adj)
        return self

    def add_total(
        self,
        category_code: str,
        category_system: str,
        value: float,
        display: Optional[str] = None
    ) -> "ExplanationOfBenefitBuilder":
        self._data.setdefault("total", [])
        total: dict = {"category": {"coding": [{"code": category_code, "system": category_system}]}, "amount": {"value": value}}
        if display:
            total["category"]["coding"][0]["display"] = display
        self._data["total"].append(total)
        return self
