"""GenomicStudyParser — parses FHIR GenomicStudy resource."""
from __future__ import annotations

from typing import Any, Optional


class GenomicStudyParser:
    def __init__(self, genomic_study: Optional[dict[str, Any]] = None) -> None:
        self.genomic_study: dict[str, Any] = (
            genomic_study if isinstance(genomic_study, dict) else {}
        )

    def get_identifiers(self) -> Any:
        return self.genomic_study.get("identifier")

    getIdentifiers = get_identifiers

    def get_status(self) -> Any:
        return self.genomic_study.get("status")

    getStatus = get_status

    def get_types(self) -> Any:
        return self.genomic_study.get("type")

    getTypes = get_types

    def get_subject_reference(self) -> Optional[str]:
        subj = self.genomic_study.get("subject")
        return subj.get("reference") if isinstance(subj, dict) else None

    getSubjectReference = get_subject_reference

    def get_encounter_reference(self) -> Optional[str]:
        enc = self.genomic_study.get("encounter")
        return enc.get("reference") if isinstance(enc, dict) else None

    getEncounterReference = get_encounter_reference

    def get_start_date(self) -> Any:
        return self.genomic_study.get("startDate")

    getStartDate = get_start_date

    def get_based_on_references(self) -> Any:
        return self.genomic_study.get("basedOn")

    getBasedOnReferences = get_based_on_references

    def get_referrer_reference(self) -> Optional[str]:
        ref = self.genomic_study.get("referrer")
        return ref.get("reference") if isinstance(ref, dict) else None

    getReferrerReference = get_referrer_reference

    def get_interpreter_references(self) -> Any:
        return self.genomic_study.get("interpreter")

    getInterpreterReferences = get_interpreter_references

    def get_reasons(self) -> Any:
        return self.genomic_study.get("reason")

    getReasons = get_reasons

    def get_notes(self) -> Any:
        return self.genomic_study.get("note")

    getNotes = get_notes

    def get_description(self) -> Any:
        return self.genomic_study.get("description")

    getDescription = get_description

    def get_analyses(self) -> Any:
        return self.genomic_study.get("analysis")

    getAnalyses = get_analyses

    def get_performers(self) -> Any:
        return self.genomic_study.get("performer")

    getPerformers = get_performers
