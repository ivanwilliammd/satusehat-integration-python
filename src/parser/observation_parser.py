"""ObservationParser — parses FHIR Observation resource."""
from __future__ import annotations

from typing import Any, Optional


def _remove_prefix(value: Optional[str], prefix: str) -> Optional[str]:
    if value and isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class ObservationParser:
    def __init__(self, observation: Optional[dict[str, Any]] = None) -> None:
        self.observation: dict[str, Any] = observation if isinstance(observation, dict) else {}

    def get_status(self) -> Any:
        return self.observation.get("status")

    getStatus = get_status

    def get_categories(self) -> Any:
        return self.observation.get("category")

    getCategories = get_categories

    def get_code(self) -> Any:
        return self.observation.get("code")

    getCode = get_code

    def get_subject(self) -> Any:
        return self.observation.get("subject")

    getSubject = get_subject

    def get_subject_reference(self) -> Optional[str]:
        subj = self.observation.get("subject")
        ref = subj.get("reference") if isinstance(subj, dict) else None
        return _remove_prefix(ref, "Patient/")

    getSubjectReference = get_subject_reference

    def get_encounter(self) -> Any:
        return self.observation.get("encounter")

    getEncounter = get_encounter

    def get_encounter_reference(self) -> Optional[str]:
        enc = self.observation.get("encounter")
        ref = enc.get("reference") if isinstance(enc, dict) else None
        return _remove_prefix(ref, "Encounter/")

    getEncounterReference = get_encounter_reference

    def get_effective_date_time(self) -> Any:
        return self.observation.get("effectiveDateTime")

    getEffectiveDateTime = get_effective_date_time

    def get_issued(self) -> Any:
        return self.observation.get("issued")

    getIssued = get_issued

    def get_performers(self) -> Any:
        return self.observation.get("performer")

    getPerformers = get_performers

    def get_performer_references(self) -> list[Optional[str]]:
        performers = self.observation.get("performer") or []
        return [
            _remove_prefix(p.get("reference") if isinstance(p, dict) else None, "Practitioner/")
            for p in performers
        ]

    getPerformerReferences = get_performer_references

    def get_value_quantity(self) -> Any:
        return self.observation.get("valueQuantity")

    getValueQuantity = get_value_quantity

    def get_value_string(self) -> Any:
        return self.observation.get("valueString")

    getValueString = get_value_string

    def get_value_codeable_concept(self) -> Any:
        return self.observation.get("valueCodeableConcept")

    getValueCodeableConcept = get_value_codeable_concept

    def get_based_on(self) -> Any:
        return self.observation.get("basedOn")

    getBasedOn = get_based_on

    def get_specimen(self) -> Any:
        return self.observation.get("specimen")

    getSpecimen = get_specimen

    def get_specimen_reference(self) -> Optional[str]:
        spec = self.observation.get("specimen")
        ref = spec.get("reference") if isinstance(spec, dict) else None
        return _remove_prefix(ref, "Specimen/")

    getSpecimenReference = get_specimen_reference

    def get_interpretations(self) -> Any:
        return self.observation.get("interpretation")

    getInterpretations = get_interpretations

    def get_reference_ranges(self) -> Any:
        return self.observation.get("referenceRange")

    getReferenceRanges = get_reference_ranges

    def get_derived_from(self) -> Any:
        return self.observation.get("derivedFrom")

    getDerivedFrom = get_derived_from

    def get_components(self) -> Any:
        return self.observation.get("component")

    getComponents = get_components

    def get_identifiers(self) -> Any:
        return self.observation.get("identifier")

    getIdentifiers = get_identifiers

    def get_part_of(self) -> Any:
        return self.observation.get("partOf")

    getPartOf = get_part_of

    def get_method(self) -> Any:
        return self.observation.get("method")

    getMethod = get_method

    def get_note(self) -> Any:
        return self.observation.get("note")

    getNote = get_note
