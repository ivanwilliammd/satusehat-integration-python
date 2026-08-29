"""Claim resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class ClaimBuilder(BaseBuilder):
    """Builder for Claim resource."""

    def __init__(self):
        super().__init__("Claim")
    def set_id(self, id: str) -> "ClaimBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "ClaimBuilder":
        self.data["status"] = status
        return self

    def set_type(self, code: str, system: str, display: Optional[str] = None) -> "ClaimBuilder":
        self.data["type"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["type"]["coding"][0]["display"] = display
        return self

    def set_sub_type(self, code: str, system: str, display: Optional[str] = None) -> "ClaimBuilder":
        self.data["subType"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["subType"]["coding"][0]["display"] = display
        return self

    def set_use(self, use: str) -> "ClaimBuilder":
        self.data["use"] = use
        return self

    def set_priority(self, code: str, system: str, display: Optional[str] = None) -> "ClaimBuilder":
        self.data["priority"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["priority"]["coding"][0]["display"] = display
        return self

    def set_patient(self, reference: str, display: Optional[str] = None) -> "ClaimBuilder":
        self.data["patient"] = {"reference": reference}
        if display:
            self.data["patient"]["display"] = display
        return self

    def set_billable_period(self, start: Optional[str] = None, end: Optional[str] = None) -> "ClaimBuilder":
        period: dict = {}
        if start:
            period["start"] = start
        if end:
            period["end"] = end
        self.data["billablePeriod"] = period
        return self

    def set_created(self, created: str) -> "ClaimBuilder":
        self.data["created"] = created
        return self

    def set_insurer(self, reference: str, display: Optional[str] = None) -> "ClaimBuilder":
        self.data["insurer"] = {"reference": reference}
        if display:
            self.data["insurer"]["display"] = display
        return self

    def set_provider(self, reference: str, display: Optional[str] = None) -> "ClaimBuilder":
        self.data["provider"] = {"reference": reference}
        if display:
            self.data["provider"]["display"] = display
        return self

    def set_priority_code(self, code: str, system: str = "http://hl7.org/fhir/request-priority") -> "ClaimBuilder":
        self.data["priority"] = {"coding": [{"system": system, "code": code}]}
        return self

    def add_supporting_info(self, sequence: int, code: str, code_system: str, value: Optional[str] = None) -> "ClaimBuilder":
        self.data.setdefault("supportingInfo", [])
        info: dict = {"sequence": sequence, "category": {"coding": [{"code": code, "system": code_system}]}}
        if value:
            info["valueString"] = value
        self.data["supportingInfo"].append(info)
        return self

    def add_diagnosis(
        self,
        sequence: int,
        diagnosis_code: str,
        diagnosis_system: str,
        type_code: Optional[str] = None,
        type_system: Optional[str] = None
    ) -> "ClaimBuilder":
        self.data.setdefault("diagnosis", [])
        diag: dict = {
            "sequence": sequence,
            "diagnosisCodeableConcept": {"coding": [{"code": diagnosis_code, "system": diagnosis_system}]}
        }
        if type_code:
            diag["type"] = [{"coding": [{"code": type_code, "system": type_system or "http://hl7.org/fhir/ex-diagnosistype"}]}]
        self.data["diagnosis"].append(diag)
        return self

    def add_insurance(
        self,
        sequence: int,
        coverage_reference: str,
        focal: bool = False,
        coverage_display: Optional[str] = None
    ) -> "ClaimBuilder":
        self.data.setdefault("insurance", [])
        ins: dict = {
            "sequence": str(sequence),
            "coverage": {"reference": coverage_reference},
            "focal": focal
        }
        if coverage_display:
            ins["coverage"]["display"] = coverage_display
        self.data["insurance"].append(ins)
        return self

    def add_item(
        self,
        sequence: int,
        service_code: str,
        service_system: str,
        serviced_date: Optional[str] = None
    ) -> "ClaimBuilder":
        self.data.setdefault("item", [])
        item: dict = {
            "sequence": sequence,
            "service": {"coding": [{"code": service_code, "system": service_system}]}
        }
        if serviced_date:
            item["servicedDate"] = serviced_date
        self.data["item"].append(item)
        return self

    def add_item_encounter(self, item_index: int, encounter_reference: str) -> "ClaimBuilder":
        if "item" in self.data and len(self.data["item"]) > item_index:
            self.data["item"][item_index].setdefault("encounter", [])
            self.data["item"][item_index]["encounter"].append({"reference": encounter_reference})
        return self
