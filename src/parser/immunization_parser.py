"""ImmunizationParser — typed accessors over the official SATUSEHAT Immunization payload.

Shape source: satusehat-conformance/examples/satusehat/Immunization.json, copied unchanged to
src/parser/testdata/Immunization.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class ImmunizationParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_vaccine_code(self) -> Any:
        return self.payload.get("vaccineCode")

    getVaccineCode = get_vaccine_code

    def get_patient(self) -> Any:
        return self.payload.get("patient")

    getPatient = get_patient

    def get_encounter(self) -> Any:
        return self.payload.get("encounter")

    getEncounter = get_encounter

    def get_occurrence_date_time(self) -> Any:
        return self.payload.get("occurrenceDateTime")

    getOccurrenceDateTime = get_occurrence_date_time

    def get_recorded(self) -> Any:
        return self.payload.get("recorded")

    getRecorded = get_recorded

    def get_reaction(self) -> Any:
        return self.payload.get("reaction")

    getReaction = get_reaction

    def get_primary_source(self) -> Any:
        return self.payload.get("primarySource")

    getPrimarySource = get_primary_source

    def get_location(self) -> Any:
        return self.payload.get("location")

    getLocation = get_location

    def get_lot_number(self) -> Any:
        return self.payload.get("lotNumber")

    getLotNumber = get_lot_number

    def get_expiration_date(self) -> Any:
        return self.payload.get("expirationDate")

    getExpirationDate = get_expiration_date

    def get_route(self) -> Any:
        return self.payload.get("route")

    getRoute = get_route

    def get_dose_quantity(self) -> Any:
        return self.payload.get("doseQuantity")

    getDoseQuantity = get_dose_quantity

    def get_performer(self) -> Any:
        return self.payload.get("performer")

    getPerformer = get_performer

    def get_reason_code(self) -> Any:
        return self.payload.get("reasonCode")

    getReasonCode = get_reason_code

    def get_protocol_applied(self) -> Any:
        return self.payload.get("protocolApplied")

    getProtocolApplied = get_protocol_applied

    def get_subject(self) -> Any:
        return self._data.get("subject")

    getSubject = get_subject

    def get_report_origin(self) -> Any:
        return self._data.get("reportOrigin")

    getReportOrigin = get_report_origin

    def get_manufacturer(self) -> Any:
        return self._data.get("manufacturer")

    getManufacturer = get_manufacturer

    def get_site(self) -> Any:
        return self._data.get("site")

    getSite = get_site

    def get_reason_reference(self) -> Any:
        return self._data.get("reasonReference")

    getReasonReference = get_reason_reference

    def get_is_subpotent(self) -> Any:
        return self._data.get("isSubpotent")

    getIsSubpotent = get_is_subpotent

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_note(self) -> Any:
        return self._data.get("note")

    getNote = get_note

    def get_subpotent_reason(self) -> Any:
        return self._data.get("subpotentReason")

    getSubpotentReason = get_subpotent_reason
