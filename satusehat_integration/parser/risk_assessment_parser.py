"""RiskAssessmentParser — parses FHIR RiskAssessment resource."""
from __future__ import annotations

from typing import Any, Optional


def _remove_prefix(value: Optional[str], prefix: str) -> Optional[str]:
    if value and isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class RiskAssessmentParser:
    def __init__(self, risk_assessment: Optional[dict[str, Any]] = None) -> None:
        self.risk_assessment: dict[str, Any] = (
            risk_assessment if isinstance(risk_assessment, dict) else {}
        )

    def get_status(self) -> Any:
        return self.risk_assessment.get("status")

    getStatus = get_status

    def get_identifiers(self) -> Any:
        return self.risk_assessment.get("identifier")

    getIdentifiers = get_identifiers

    def get_code(self) -> Any:
        return self.risk_assessment.get("code")

    getCode = get_code

    def get_subject(self) -> Any:
        return self.risk_assessment.get("subject")

    getSubject = get_subject

    def get_subject_reference(self) -> Optional[str]:
        subj = self.risk_assessment.get("subject")
        ref = subj.get("reference") if isinstance(subj, dict) else None
        return _remove_prefix(ref, "Patient/")

    getSubjectReference = get_subject_reference

    def get_encounter(self) -> Any:
        return self.risk_assessment.get("encounter")

    getEncounter = get_encounter

    def get_encounter_reference(self) -> Optional[str]:
        enc = self.risk_assessment.get("encounter")
        ref = enc.get("reference") if isinstance(enc, dict) else None
        return _remove_prefix(ref, "Encounter/")

    getEncounterReference = get_encounter_reference

    def get_occurrence_date_time(self) -> Any:
        return self.risk_assessment.get("occurrenceDateTime")

    getOccurrenceDateTime = get_occurrence_date_time

    def get_condition(self) -> Any:
        return self.risk_assessment.get("condition")

    getCondition = get_condition

    def get_condition_reference(self) -> Optional[str]:
        cond = self.risk_assessment.get("condition")
        ref = cond.get("reference") if isinstance(cond, dict) else None
        return _remove_prefix(ref, "Condition/")

    getConditionReference = get_condition_reference

    def get_performer(self) -> Any:
        return self.risk_assessment.get("performer")

    getPerformer = get_performer

    def get_performer_reference(self) -> Optional[str]:
        perf = self.risk_assessment.get("performer")
        ref = perf.get("reference") if isinstance(perf, dict) else None
        return _remove_prefix(ref, "Practitioner/")

    getPerformerReference = get_performer_reference

    def get_reason_references(self) -> Any:
        return self.risk_assessment.get("reasonReference")

    getReasonReferences = get_reason_references

    def get_basis(self) -> Any:
        return self.risk_assessment.get("basis")

    getBasis = get_basis

    def get_predictions(self) -> Any:
        return self.risk_assessment.get("prediction")

    getPredictions = get_predictions

    def get_mitigation(self) -> Any:
        return self.risk_assessment.get("mitigation")

    getMitigation = get_mitigation

    def get_notes(self) -> Any:
        return self.risk_assessment.get("note")

    getNotes = get_notes
