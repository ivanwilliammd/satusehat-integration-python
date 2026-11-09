"""ServiceRequestParser — parses FHIR ServiceRequest resource."""
from __future__ import annotations

from typing import Any, Optional


def _remove_prefix(value: Optional[str], prefix: str) -> Optional[str]:
    if value and isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class ServiceRequestParser:
    def __init__(self, service_request: Optional[dict[str, Any]] = None) -> None:
        self.service_request: dict[str, Any] = (
            service_request if isinstance(service_request, dict) else {}
        )

    def get_identifiers(self) -> Any:
        return self.service_request.get("identifier")

    getIdentifiers = get_identifiers

    def get_requisition(self) -> Any:
        return self.service_request.get("requisition")

    getRequisition = get_requisition

    def get_status(self) -> Any:
        return self.service_request.get("status")

    getStatus = get_status

    def get_intent(self) -> Any:
        return self.service_request.get("intent")

    getIntent = get_intent

    def get_categories(self) -> Any:
        return self.service_request.get("category")

    getCategories = get_categories

    def get_priority(self) -> Any:
        return self.service_request.get("priority")

    getPriority = get_priority

    def get_do_not_perform(self) -> Any:
        return self.service_request.get("doNotPerform")

    getDoNotPerform = get_do_not_perform

    def get_code(self) -> Any:
        return self.service_request.get("code")

    getCode = get_code

    def get_quantity_quantity(self) -> Any:
        return self.service_request.get("quantityQuantity")

    getQuantityQuantity = get_quantity_quantity

    def get_subject_reference(self) -> Optional[str]:
        subj = self.service_request.get("subject")
        return subj.get("reference") if isinstance(subj, dict) else None

    getSubjectReference = get_subject_reference

    def get_subject_display(self) -> Optional[str]:
        subj = self.service_request.get("subject")
        return subj.get("display") if isinstance(subj, dict) else None

    getSubjectDisplay = get_subject_display

    def get_encounter_reference(self) -> Optional[str]:
        enc = self.service_request.get("encounter")
        ref = enc.get("reference") if isinstance(enc, dict) else None
        return _remove_prefix(ref, "Encounter/")

    getEncounterReference = get_encounter_reference

    def get_encounter_display(self) -> Optional[str]:
        enc = self.service_request.get("encounter")
        return enc.get("display") if isinstance(enc, dict) else None

    getEncounterDisplay = get_encounter_display

    def get_occurrence_date_time(self) -> Any:
        return self.service_request.get("occurrenceDateTime")

    getOccurrenceDateTime = get_occurrence_date_time

    def get_authored_on(self) -> Any:
        return self.service_request.get("authoredOn")

    getAuthoredOn = get_authored_on

    def get_requester_reference(self) -> Optional[str]:
        req = self.service_request.get("requester")
        return req.get("reference") if isinstance(req, dict) else None

    getRequesterReference = get_requester_reference

    def get_requester_display(self) -> Optional[str]:
        req = self.service_request.get("requester")
        return req.get("display") if isinstance(req, dict) else None

    getRequesterDisplay = get_requester_display

    def get_performers(self) -> Any:
        return self.service_request.get("performer")

    getPerformers = get_performers

    def get_reason_codes(self) -> Any:
        return self.service_request.get("reasonCode")

    getReasonCodes = get_reason_codes

    def get_supporting_info(self) -> Any:
        return self.service_request.get("supportingInfo")

    getSupportingInfo = get_supporting_info

    def get_specimens(self) -> Any:
        return self.service_request.get("specimen")

    getSpecimens = get_specimens

    def get_notes(self) -> Any:
        return self.service_request.get("note")

    getNotes = get_notes

    def get_patient_instruction(self) -> Any:
        return self.service_request.get("patientInstruction")

    getPatientInstruction = get_patient_instruction

    def get_relevant_history(self) -> Any:
        return self.service_request.get("relevantHistory")

    getRelevantHistory = get_relevant_history
