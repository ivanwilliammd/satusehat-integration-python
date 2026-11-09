"""DiagnosticReportParser — parses FHIR DiagnosticReport resource."""
from __future__ import annotations

from typing import Any, Optional


def _remove_prefix(value: Optional[str], prefix: str) -> Optional[str]:
    if value and isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class DiagnosticReportParser:
    def __init__(self, diagnostic_report: Optional[dict[str, Any]] = None) -> None:
        self.diagnostic_report: dict[str, Any] = (
            diagnostic_report if isinstance(diagnostic_report, dict) else {}
        )

    def get_identifiers(self) -> Any:
        return self.diagnostic_report.get("identifier")

    getIdentifiers = get_identifiers

    def get_status(self) -> Any:
        return self.diagnostic_report.get("status")

    getStatus = get_status

    def get_categories(self) -> Any:
        return self.diagnostic_report.get("category")

    getCategories = get_categories

    def get_code(self) -> Any:
        return self.diagnostic_report.get("code")

    getCode = get_code

    def get_subject(self) -> Any:
        return self.diagnostic_report.get("subject")

    getSubject = get_subject

    def get_subject_reference(self) -> Optional[str]:
        subj = self.diagnostic_report.get("subject")
        ref = subj.get("reference") if isinstance(subj, dict) else None
        return _remove_prefix(ref, "Patient/")

    getSubjectReference = get_subject_reference

    def get_encounter(self) -> Any:
        return self.diagnostic_report.get("encounter")

    getEncounter = get_encounter

    def get_encounter_reference(self) -> Optional[str]:
        enc = self.diagnostic_report.get("encounter")
        ref = enc.get("reference") if isinstance(enc, dict) else None
        return _remove_prefix(ref, "Encounter/")

    getEncounterReference = get_encounter_reference

    def get_effective_date_time(self) -> Any:
        return self.diagnostic_report.get("effectiveDateTime")

    getEffectiveDateTime = get_effective_date_time

    def get_issued(self) -> Any:
        return self.diagnostic_report.get("issued")

    getIssued = get_issued

    def get_performers(self) -> Any:
        return self.diagnostic_report.get("performer")

    getPerformers = get_performers

    def get_performer_references(self) -> list[Optional[str]]:
        performers = self.diagnostic_report.get("performer") or []
        return [
            _remove_prefix(p.get("reference") if isinstance(p, dict) else None, "Practitioner/")
            for p in performers
        ]

    getPerformerReferences = get_performer_references

    def get_results(self) -> Any:
        return self.diagnostic_report.get("result")

    getResults = get_results

    def get_result_references(self) -> list[Optional[str]]:
        results = self.diagnostic_report.get("result") or []
        return [
            _remove_prefix(r.get("reference") if isinstance(r, dict) else None, "Observation/")
            for r in results
        ]

    getResultReferences = get_result_references

    def get_specimens(self) -> Any:
        return self.diagnostic_report.get("specimen")

    getSpecimens = get_specimens

    def get_specimen_references(self) -> list[Optional[str]]:
        specimens = self.diagnostic_report.get("specimen") or []
        return [
            _remove_prefix(s.get("reference") if isinstance(s, dict) else None, "Specimen/")
            for s in specimens
        ]

    getSpecimenReferences = get_specimen_references

    def get_conclusion_codes(self) -> Any:
        return self.diagnostic_report.get("conclusionCode")

    getConclusionCodes = get_conclusion_codes

    def get_based_on(self) -> Any:
        return self.diagnostic_report.get("basedOn")

    getBasedOn = get_based_on

    def get_conclusion(self) -> Any:
        return self.diagnostic_report.get("conclusion")

    getConclusion = get_conclusion
