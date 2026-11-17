"""ProcedureParser — parses FHIR Procedure resource."""
from __future__ import annotations

from typing import Any, Optional


def _remove_prefix(value: Optional[str], prefix: str) -> Optional[str]:
    if value and isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class ProcedureParser:
    def __init__(self, procedure: Optional[dict[str, Any]] = None) -> None:
        self.procedure: dict[str, Any] = procedure if isinstance(procedure, dict) else {}

    def get_identifiers(self) -> Any:
        return self.procedure.get("identifier")

    getIdentifiers = get_identifiers

    def get_status(self) -> Any:
        return self.procedure.get("status")

    getStatus = get_status

    def get_category(self) -> Any:
        return self.procedure.get("category")

    getCategory = get_category

    def get_code(self) -> Any:
        return self.procedure.get("code")

    getCode = get_code

    def get_subject(self) -> Any:
        return self.procedure.get("subject")

    getSubject = get_subject

    def get_subject_reference(self) -> Optional[str]:
        subj = self.procedure.get("subject")
        ref = subj.get("reference") if isinstance(subj, dict) else None
        return _remove_prefix(ref, "Patient/")

    getSubjectReference = get_subject_reference

    def get_subject_display(self) -> Optional[str]:
        subj = self.procedure.get("subject")
        return subj.get("display") if isinstance(subj, dict) else None

    getSubjectDisplay = get_subject_display

    def get_encounter(self) -> Any:
        return self.procedure.get("encounter")

    getEncounter = get_encounter

    def get_encounter_reference(self) -> Optional[str]:
        enc = self.procedure.get("encounter")
        ref = enc.get("reference") if isinstance(enc, dict) else None
        return _remove_prefix(ref, "Encounter/")

    getEncounterReference = get_encounter_reference

    def get_encounter_display(self) -> Optional[str]:
        enc = self.procedure.get("encounter")
        return enc.get("display") if isinstance(enc, dict) else None

    getEncounterDisplay = get_encounter_display

    def get_performers(self) -> Any:
        return self.procedure.get("performer")

    getPerformers = get_performers

    def get_performer_references(self) -> list[Optional[str]]:
        performers = self.procedure.get("performer") or []
        return [
            _remove_prefix(
                (p.get("actor") or {}).get("reference") if isinstance(p, dict) else None,
                "Practitioner/",
            )
            for p in performers
        ]

    getPerformerReferences = get_performer_references

    def get_performer_displays(self) -> list[Optional[str]]:
        performers = self.procedure.get("performer") or []
        return [
            (p.get("actor") or {}).get("display") if isinstance(p, dict) else None
            for p in performers
        ]

    getPerformerDisplays = get_performer_displays

    def get_performed_period(self) -> Any:
        return self.procedure.get("performedPeriod")

    getPerformedPeriod = get_performed_period

    def get_reason_codes(self) -> Any:
        return self.procedure.get("reasonCode")

    getReasonCodes = get_reason_codes

    def get_body_sites(self) -> Any:
        return self.procedure.get("bodySite")

    getBodySites = get_body_sites

    def get_notes(self) -> Any:
        return self.procedure.get("note")

    getNotes = get_notes

    def get_used_codes(self) -> Any:
        return self.procedure.get("usedCode")

    getUsedCodes = get_used_codes

    def get_based_on(self) -> Any:
        return self.procedure.get("basedOn")

    getBasedOn = get_based_on

    def get_location(self) -> Optional[str]:
        loc = self.procedure.get("location")
        ref = loc.get("reference") if isinstance(loc, dict) else None
        return _remove_prefix(ref, "Location/")

    getLocation = get_location
