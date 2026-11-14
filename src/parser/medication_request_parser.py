"""MedicationRequestParser — typed accessors over the official SATUSEHAT MedicationRequest payload.

Shape source: satusehat-conformance/examples/satusehat/MedicationRequest.json, copied unchanged to
src/parser/testdata/MedicationRequest.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class MedicationRequestParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_contained(self) -> Any:
        return self.payload.get("contained")

    getContained = get_contained

    def get_identifier(self) -> Any:
        return self.payload.get("identifier")

    getIdentifier = get_identifier

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_intent(self) -> Any:
        return self.payload.get("intent")

    getIntent = get_intent

    def get_category(self) -> Any:
        return self.payload.get("category")

    getCategory = get_category

    def get_priority(self) -> Any:
        return self.payload.get("priority")

    getPriority = get_priority

    def get_medication_reference(self) -> Any:
        return self.payload.get("medicationReference")

    getMedicationReference = get_medication_reference

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_encounter(self) -> Any:
        return self.payload.get("encounter")

    getEncounter = get_encounter

    def get_authored_on(self) -> Any:
        return self.payload.get("authoredOn")

    getAuthoredOn = get_authored_on

    def get_requester(self) -> Any:
        return self.payload.get("requester")

    getRequester = get_requester

    def get_course_of_therapy_type(self) -> Any:
        return self.payload.get("courseOfTherapyType")

    getCourseOfTherapyType = get_course_of_therapy_type

    def get_dosage_instruction(self) -> Any:
        return self.payload.get("dosageInstruction")

    getDosageInstruction = get_dosage_instruction

    def get_dispense_request(self) -> Any:
        return self.payload.get("dispenseRequest")

    getDispenseRequest = get_dispense_request
