from typing import Any, Dict, List, Optional

from src.builder.base_builder import BaseBuilder


class ServiceRequestBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("ServiceRequest")

    def add_identifier(self, system: str, value: str) -> "ServiceRequestBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append({"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "ServiceRequestBuilder":
        self.data["status"] = status
        return self

    def set_intent(self, intent: str) -> "ServiceRequestBuilder":
        self.data["intent"] = intent
        return self

    def set_priority(self, priority: str) -> "ServiceRequestBuilder":
        self.data["priority"] = priority
        return self

    def set_code(
        self,
        code: str,
        display: str,
        system: str = "http://snomed.info/sct",
    ) -> "ServiceRequestBuilder":
        self.data["code"] = {
            "coding": [{"system": system, "code": code, "display": display}]
        }
        return self

    def set_subject(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ServiceRequestBuilder":
        subj: Dict[str, Any] = {"reference": reference}
        if display:
            subj["display"] = display
        self.data["subject"] = subj
        return self

    def set_encounter(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ServiceRequestBuilder":
        enc: Dict[str, Any] = {"reference": reference}
        if display:
            enc["display"] = display
        self.data["encounter"] = enc
        return self

    def set_authored_on(self, authored_on: str) -> "ServiceRequestBuilder":
        self.data["authoredOn"] = authored_on
        return self

    def set_requester(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ServiceRequestBuilder":
        req: Dict[str, Any] = {"reference": reference}
        if display:
            req["display"] = display
        self.data["requester"] = req
        return self

    def add_performer(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ServiceRequestBuilder":
        if "performer" not in self.data:
            self.data["performer"] = []
        perf: Dict[str, Any] = {"reference": reference}
        if display:
            perf["display"] = display
        self.data["performer"].append(perf)
        return self

    def set_occurrence(self, occurrence: str) -> "ServiceRequestBuilder":
        self.data["occurrenceDateTime"] = occurrence
        return self

    def add_note(
        self,
        text: str,
        author_ref: Optional[str] = None,
    ) -> "ServiceRequestBuilder":
        if "note" not in self.data:
            self.data["note"] = []
        note: Dict[str, Any] = {"text": text}
        if author_ref:
            note["authorReference"] = {"reference": author_ref}
        self.data["note"].append(note)
        return self

    def add_reason(
        self,
        code: str,
        display: str,
        system: str = "http://snomed.info/sct",
    ) -> "ServiceRequestBuilder":
        if "reasonCode" not in self.data:
            self.data["reasonCode"] = []
        self.data["reasonCode"].append({
            "coding": [{"system": system, "code": code, "display": display}]
        })
        return self
