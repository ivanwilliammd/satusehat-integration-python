from typing import Any, Dict, List, Optional

from src.builder.base_builder import BaseBuilder


def _arr(value: Any) -> Any:
    return value.to_array() if hasattr(value, "to_array") else value


class ServiceRequestBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("ServiceRequest")

    def set_id(self, id: str) -> "ServiceRequestBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "ServiceRequestBuilder":
        if value is not None:
            return self._push("identifier", {"system": identifier, "value": value})
        return self._push("identifier", _arr(identifier))

    def set_requisition(self, requisition: Any, value: Optional[str] = None) -> "ServiceRequestBuilder":
        if value is not None:
            self.data["requisition"] = {"system": requisition, "value": value}
        else:
            self.data["requisition"] = _arr(requisition)
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
        code: Any,
        display: Optional[str] = None,
        system: str = "http://snomed.info/sct",
    ) -> "ServiceRequestBuilder":
        if isinstance(code, str):
            self.data["code"] = {"coding": [{"system": system, "code": code, "display": display or code}]}
        else:
            self.data["code"] = _arr(code)
        return self

    def add_category(self, category: Any) -> "ServiceRequestBuilder":
        return self._push("category", _arr(category))

    def set_do_not_perform(self, do_not_perform: bool) -> "ServiceRequestBuilder":
        self.data["doNotPerform"] = do_not_perform
        return self

    def set_quantity_quantity(self, quantity: Any) -> "ServiceRequestBuilder":
        self.data["quantityQuantity"] = _arr(quantity)
        return self

    def set_occurrence_date_time(self, date_time: str) -> "ServiceRequestBuilder":
        self.data["occurrenceDateTime"] = date_time
        return self

    def add_reason_code(self, reason_code: Any) -> "ServiceRequestBuilder":
        return self._push("reasonCode", _arr(reason_code))

    def add_supporting_info(self, supporting_info: Any) -> "ServiceRequestBuilder":
        return self._push("supportingInfo", _arr(supporting_info))

    def add_specimen(self, specimen: Any) -> "ServiceRequestBuilder":
        return self._push("specimen", _arr(specimen))

    def set_patient_instruction(self, instruction: str) -> "ServiceRequestBuilder":
        self.data["patientInstruction"] = instruction
        return self

    def add_relevant_history(self, relevant_history: Any) -> "ServiceRequestBuilder":
        return self._push("relevantHistory", _arr(relevant_history))

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "ServiceRequestBuilder":
        extension: Dict[str, Any] = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        return self._push("extension", extension)

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
