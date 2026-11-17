"""MedicationAdministrationParser — typed accessors over the official SATUSEHAT MedicationAdministration payload.

Shape source: satusehat-conformance/examples/satusehat/MedicationAdministration.json, copied unchanged to
satusehat_integration/parser/testdata/MedicationAdministration.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class MedicationAdministrationParser:
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

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_category(self) -> Any:
        return self.payload.get("category")

    getCategory = get_category

    def get_medication_reference(self) -> Any:
        return self.payload.get("medicationReference")

    getMedicationReference = get_medication_reference

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_context(self) -> Any:
        return self.payload.get("context")

    getContext = get_context

    def get_effective_period(self) -> Any:
        return self.payload.get("effectivePeriod")

    getEffectivePeriod = get_effective_period

    def get_performer(self) -> Any:
        return self.payload.get("performer")

    getPerformer = get_performer

    def get_reason_code(self) -> Any:
        return self.payload.get("reasonCode")

    getReasonCode = get_reason_code

    def get_request(self) -> Any:
        return self.payload.get("request")

    getRequest = get_request

    def get_dosage(self) -> Any:
        return self.payload.get("dosage")

    getDosage = get_dosage

    def get_medication(self) -> Any:
        return self._data.get("medication")

    getMedication = get_medication

    def get_encounter(self) -> Any:
        return self._data.get("encounter")

    getEncounter = get_encounter

    def get_effective_date_time(self) -> Any:
        return self._data.get("effectiveDateTime")

    getEffectiveDateTime = get_effective_date_time

    def get_requester(self) -> Any:
        return self._data.get("requester")

    getRequester = get_requester

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id
