"""ClinicalImpressionParser — typed accessors over the official SATUSEHAT ClinicalImpression payload.

Shape source: satusehat-conformance/examples/satusehat/ClinicalImpression.json, copied unchanged to
satusehat_integration/parser/testdata/ClinicalImpression.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class ClinicalImpressionParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_identifier(self) -> Any:
        return self.payload.get("identifier")

    getIdentifier = get_identifier

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_code(self) -> Any:
        return self.payload.get("code")

    getCode = get_code

    def get_description(self) -> Any:
        return self.payload.get("description")

    getDescription = get_description

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_encounter(self) -> Any:
        return self.payload.get("encounter")

    getEncounter = get_encounter

    def get_effective_date_time(self) -> Any:
        return self.payload.get("effectiveDateTime")

    getEffectiveDateTime = get_effective_date_time

    def get_date(self) -> Any:
        return self.payload.get("date")

    getDate = get_date

    def get_assessor(self) -> Any:
        return self.payload.get("assessor")

    getAssessor = get_assessor

    def get_problem(self) -> Any:
        return self.payload.get("problem")

    getProblem = get_problem

    def get_investigation(self) -> Any:
        return self.payload.get("investigation")

    getInvestigation = get_investigation

    def get_summary(self) -> Any:
        return self.payload.get("summary")

    getSummary = get_summary

    def get_finding(self) -> Any:
        return self.payload.get("finding")

    getFinding = get_finding

    def get_prognosis_codeable_concept(self) -> Any:
        return self.payload.get("prognosisCodeableConcept")

    getPrognosisCodeableConcept = get_prognosis_codeable_concept
