"""ClaimResponse resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class ClaimResponseBuilder(BaseBuilder):
    """Builder for ClaimResponse resource."""

    def __init__(self):
        super().__init__("ClaimResponse")
    def set_id(self, id: str) -> "ClaimResponseBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "ClaimResponseBuilder":
        self.data["status"] = status
        return self

    def set_type(self, code: str, system: str, display: Optional[str] = None) -> "ClaimResponseBuilder":
        self.data["type"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["type"]["coding"][0]["display"] = display
        return self

    def set_sub_type(self, code: str, system: str, display: Optional[str] = None) -> "ClaimResponseBuilder":
        self.data["subType"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["subType"]["coding"][0]["display"] = display
        return self

    def set_use(self, use: str) -> "ClaimResponseBuilder":
        self.data["use"] = use
        return self

    def set_patient(self, reference: str, display: Optional[str] = None) -> "ClaimResponseBuilder":
        self.data["patient"] = {"reference": reference}
        if display:
            self.data["patient"]["display"] = display
        return self

    def set_created(self, created: str) -> "ClaimResponseBuilder":
        self.data["created"] = created
        return self

    def set_insurer(self, reference: str, display: Optional[str] = None) -> "ClaimResponseBuilder":
        self.data["insurer"] = {"reference": reference}
        if display:
            self.data["insurer"]["display"] = display
        return self

    def set_request(self, reference: str) -> "ClaimResponseBuilder":
        self.data["request"] = {"reference": reference}
        return self

    def set_outcome(self, outcome: str) -> "ClaimResponseBuilder":
        self.data["outcome"] = outcome
        return self

    def add_decision_reason(self, code: str, system: str, display: Optional[str] = None) -> "ClaimResponseBuilder":
        self.data.setdefault("decisionReason", [])
        reason: dict = {"coding": [{"system": system, "code": code}]}
        if display:
            reason["coding"][0]["display"] = display
        self.data["decisionReason"].append(reason)
        return self

    def add_communication_request(self, reference: str) -> "ClaimResponseBuilder":
        self.data.setdefault("communicationRequest", [])
        self.data["communicationRequest"].append({"reference": reference})
        return self

    def add_insurance(
        self,
        sequence: int,
        coverage_reference: str,
        focal: bool = False,
        coverage_display: Optional[str] = None
    ) -> "ClaimResponseBuilder":
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
        item_sequence: int,
        note_sequence: Optional[int] = None,
        adjudication_code: Optional[str] = None,
        adjudication_system: Optional[str] = None,
        adjudication_value: Optional[float] = None,
        adjudication_display: Optional[str] = None
    ) -> "ClaimResponseBuilder":
        self.data.setdefault("item", [])
        item: dict = {"itemSequence": item_sequence}
        if adjudication_code:
            item.setdefault("adjudication", [])
            adj: dict = {"category": {"coding": [{"code": adjudication_code, "system": adjudication_system or "http://terminology.hl7.org/CodeSystem/adjudication"}]}}
            if adjudication_value is not None:
                adj["value"] = adjudication_value
            if adjudication_display:
                adj["category"]["coding"][0]["display"] = adjudication_display
            item["adjudication"].append(adj)
        if note_sequence:
            item["noteNumber"] = [note_sequence]
        self.data["item"].append(item)
        return self
