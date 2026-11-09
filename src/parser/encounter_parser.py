"""EncounterParser — parses FHIR Encounter resource."""
from __future__ import annotations

from typing import Any, Optional


def _remove_prefix(value: Optional[str], prefix: str) -> Optional[str]:
    if value and isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class EncounterParser:
    def __init__(self, encounter: Optional[dict[str, Any]] = None) -> None:
        self.encounter: dict[str, Any] = encounter if isinstance(encounter, dict) else {}

    def get_status(self) -> Any:
        return self.encounter.get("status")

    getStatus = get_status

    def get_locations(self) -> Any:
        return self.encounter.get("location")

    getLocations = get_locations

    def get_location_references(self) -> list[Optional[str]]:
        locations = self.encounter.get("location") or []
        return [
            _remove_prefix(
                (loc.get("location") or {}).get("reference") if isinstance(loc, dict) else None,
                "Location/",
            )
            for loc in locations
        ]

    getLocationReferences = get_location_references

    def get_location_displays(self) -> list[Optional[str]]:
        locations = self.encounter.get("location") or []
        return [
            (loc.get("location") or {}).get("display") if isinstance(loc, dict) else None
            for loc in locations
        ]

    getLocationDisplays = get_location_displays

    def get_subject(self) -> Any:
        return self.encounter.get("subject")

    getSubject = get_subject

    def get_subject_reference(self) -> Optional[str]:
        subj = self.encounter.get("subject")
        ref = subj.get("reference") if isinstance(subj, dict) else None
        return _remove_prefix(ref, "Patient/")

    getSubjectReference = get_subject_reference

    def get_subject_display(self) -> Optional[str]:
        subj = self.encounter.get("subject")
        return subj.get("display") if isinstance(subj, dict) else None

    getSubjectDisplay = get_subject_display

    def get_participants(self) -> Any:
        return self.encounter.get("participant")

    getParticipants = get_participants

    def get_participant_references(self) -> list[Optional[str]]:
        participants = self.encounter.get("participant") or []
        return [
            _remove_prefix(
                (p.get("individual") or {}).get("reference") if isinstance(p, dict) else None,
                "Practitioner/",
            )
            for p in participants
        ]

    getParticipantReferences = get_participant_references

    def get_participant_displays(self) -> list[Optional[str]]:
        participants = self.encounter.get("participant") or []
        return [
            (p.get("individual") or {}).get("display") if isinstance(p, dict) else None
            for p in participants
        ]

    getParticipantDisplays = get_participant_displays

    def get_diagnosis(self) -> Any:
        return self.encounter.get("diagnosis")

    getDiagnosis = get_diagnosis

    def get_diagnosis_references(self) -> list[Optional[str]]:
        diagnoses = self.encounter.get("diagnosis") or []
        return [
            _remove_prefix(
                (d.get("condition") or {}).get("reference") if isinstance(d, dict) else None,
                "Condition/",
            )
            for d in diagnoses
        ]

    getDiagnosisReferences = get_diagnosis_references

    def get_diagnosis_displays(self) -> list[Optional[str]]:
        diagnoses = self.encounter.get("diagnosis") or []
        return [
            (d.get("condition") or {}).get("display") if isinstance(d, dict) else None
            for d in diagnoses
        ]

    getDiagnosisDisplays = get_diagnosis_displays

    def get_registration_ids(self) -> list[Optional[str]]:
        identifiers = self.encounter.get("identifier") or []
        return [i.get("value") if isinstance(i, dict) else None for i in identifiers]

    getRegistrationIds = get_registration_ids

    def get_status_history(self) -> Any:
        return self.encounter.get("statusHistory")

    getStatusHistory = get_status_history

    def get_consultation_method(self) -> Any:
        return self.encounter.get("class")

    getConsultationMethod = get_consultation_method

    def get_service_provider(self) -> Any:
        return self.encounter.get("serviceProvider")

    getServiceProvider = get_service_provider

    def get_period(self) -> Any:
        return self.encounter.get("period")

    getPeriod = get_period

    def get_period_start(self) -> Optional[str]:
        period = self.encounter.get("period")
        return period.get("start") if isinstance(period, dict) else None

    getPeriodStart = get_period_start

    def get_period_end(self) -> Optional[str]:
        period = self.encounter.get("period")
        return period.get("end") if isinstance(period, dict) else None

    getPeriodEnd = get_period_end
