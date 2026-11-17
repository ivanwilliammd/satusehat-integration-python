"""MedicationDispenseParser — typed accessors over the official SATUSEHAT MedicationDispense payload.

Shape source: satusehat-conformance/examples/satusehat/MedicationDispense.json, copied unchanged to
satusehat_integration/parser/testdata/MedicationDispense.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class MedicationDispenseParser:
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

    def get_performer(self) -> Any:
        return self.payload.get("performer")

    getPerformer = get_performer

    def get_location(self) -> Any:
        return self.payload.get("location")

    getLocation = get_location

    def get_authorizing_prescription(self) -> Any:
        return self.payload.get("authorizingPrescription")

    getAuthorizingPrescription = get_authorizing_prescription

    def get_quantity(self) -> Any:
        return self.payload.get("quantity")

    getQuantity = get_quantity

    def get_days_supply(self) -> Any:
        return self.payload.get("daysSupply")

    getDaysSupply = get_days_supply

    def get_when_prepared(self) -> Any:
        return self.payload.get("whenPrepared")

    getWhenPrepared = get_when_prepared

    def get_when_handed_over(self) -> Any:
        return self.payload.get("whenHandedOver")

    getWhenHandedOver = get_when_handed_over

    def get_dosage_instruction(self) -> Any:
        return self.payload.get("dosageInstruction")

    getDosageInstruction = get_dosage_instruction

    def get_medication(self) -> Any:
        return self._data.get("medication")

    getMedication = get_medication

    def get_encounter(self) -> Any:
        return self._data.get("encounter")

    getEncounter = get_encounter

    def get_destination(self) -> Any:
        return self._data.get("destination")

    getDestination = get_destination

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_substitution(self) -> Any:
        return self._data.get("substitution")

    getSubstitution = get_substitution
