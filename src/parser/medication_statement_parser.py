"""MedicationStatementParser — typed accessors over the official SATUSEHAT MedicationStatement payload.

Shape source: satusehat-conformance/examples/satusehat/MedicationStatement.json, copied unchanged to
src/parser/testdata/MedicationStatement.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class MedicationStatementParser:
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

    def get_dosage(self) -> Any:
        return self.payload.get("dosage")

    getDosage = get_dosage

    def get_effective_date_time(self) -> Any:
        return self.payload.get("effectiveDateTime")

    getEffectiveDateTime = get_effective_date_time

    def get_date_asserted(self) -> Any:
        return self.payload.get("dateAsserted")

    getDateAsserted = get_date_asserted

    def get_information_source(self) -> Any:
        return self.payload.get("informationSource")

    getInformationSource = get_information_source

    def get_context(self) -> Any:
        return self.payload.get("context")

    getContext = get_context
