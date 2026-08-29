"""ClaimResponse resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from .base import BaseBuilder


class ClaimResponseBuilder(BaseBuilder):
    """Builder for ClaimResponse resource."""

    def __init__(self):
        super().__init__()
        self._data = {"resourceType": "ClaimResponse"}

    def set_id(self, id: str) -> "ClaimResponseBuilder":
        self._data["id"] = id
        return self

    def set_status(self, status: str) -> "ClaimResponseBuilder":
        self._data["status"] = status
        return self

    def set_type(self, code: str, system: str, display: Optional[str] = None) -> "ClaimResponseBuilder":
        self._data["type"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self._data["type"]["coding"][0]["display"] = display
        return self

    def set_sub_type(self, code: str, system: str, display: Optional[str] = None) -> "ClaimResponseBuilder":
        self._data["subType"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self._data["subType"]["coding"][0]["display"] = display
        return self

    def set_use(self, use: str) -> "ClaimResponseBuilder":
        self._data["use"] = use
        return self

    def set_patient(self, reference: str, display: Optional[str] = None) -> "ClaimResponseBuilder":
        self._data["patient"] = {"reference": reference}
        if display:
            self._data["patient"]["display"] = display
        return self

    def set_created(self, created: str) -> "ClaimResponseBuilder":
        self._data["created"] = created
        return self

    def set_insurer(self, reference: str, display: Optional[str] = None) -> "ClaimResponseBuilder":
        self._data["insurer"] = {"reference": reference}
        if display:
            self._data["insurer"]["display"] = display
        return self

    def set_request(self, reference: str) -> "ClaimResponseBuilder":
        self._data["request"] = {"reference": reference}
        return self

    def set_outcome(self, outcome: str) -> "ClaimResponseBuilder":
        self._data["outcome"] = outcome
        return self

    def add_decision_reason(self, code: str, system: str, display: Optional[str] = None) -> "ClaimResponseBuilder":
        self._data.setdefault("decisionReason", [])
        reason: dict = {"coding": [{"system": system, "code": code}]}
        if display:
            reason["coding"][0]["display"] = display
        self._data["decisionReason"].append(reason)
        return self

    def add_communication_request(self, reference: str) -> "ClaimResponseBuilder":
        self._data.setdefault("communicationRequest", [])
        self._data["communicationRequest"].append({"reference": reference})
        return self

    def add_insurance(
        self,
        sequence: int,
        coverage_reference: str,
        focal: bool = False,
        coverage_display: Optional[str] = None
    ) -> "ClaimResponseBuilder":
        self._data.setdefault("insurance", [])
        ins: dict = {
            "sequence": str(sequence),
            "coverage": {"reference": coverage_reference},
            "focal": focal
        }
        if coverage_display:
            ins["coverage"]["display"] = coverage_display
        self._data["insurance"].append(ins)
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
        self._data.setdefault("item", [])
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
        self._data["item"].append(item)
        return self
