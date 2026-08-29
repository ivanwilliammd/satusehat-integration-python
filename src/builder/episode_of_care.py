from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class EpisodeOfCareBuilder(BaseBuilder):
    _resourceType = "EpisodeOfCare"

    def __init__(self) -> None:
        super().__init__("EpisodeOfCare")

    def status(self, value: str) -> "EpisodeOfCareBuilder":
        return self._set("status", value)

    def status_history(self, status: str, period: dict) -> "EpisodeOfCareBuilder":
        return self._append("statusHistory", {"status": status, "period": period})

    def type(self, codeable_concept: dict) -> "EpisodeOfCareBuilder":
        return self._set("type", [codeable_concept])

    def diagnosis(self, condition_reference: Optional[str] = None, condition_codeable_concept: Optional[dict] = None, rank: Optional[int] = None) -> "EpisodeOfCareBuilder":
        diag: dict = {}
        if condition_reference:
            diag["condition"] = {"reference": condition_reference}
        if condition_codeable_concept:
            diag["condition"] = condition_codeable_concept
        if rank is not None:
            diag["rank"] = rank
        return self._append("diagnosis", diag) if diag else self

    def patient(self, reference: str, display: Optional[str] = None) -> "EpisodeOfCareBuilder":
        pt: dict = {"reference": reference}
        if display:
            pt["display"] = display
        return self._set("patient", pt)

    def managing_organization(self, reference: str, display: Optional[str] = None) -> "EpisodeOfCareBuilder":
        org: dict = {"reference": reference}
        if display:
            org["display"] = display
        return self._set("managingOrganization", org)

    def period(self, start: Optional[str] = None, end: Optional[str] = None) -> "EpisodeOfCareBuilder":
        p: dict = {}
        if start:
            p["start"] = start
        if end:
            p["end"] = end
        return self._set("period", p) if p else self

    def referral_request(self, reference: str) -> "EpisodeOfCareBuilder":
        return self._append("referralRequest", {"reference": reference})

    def care_manager(self, reference: str, display: Optional[str] = None) -> "EpisodeOfCareBuilder":
        cm: dict = {"reference": reference}
        if display:
            cm["display"] = display
        return self._set("careManager", cm)

    def identifier(self, system: str, value: str) -> "EpisodeOfCareBuilder":
        return self._append("identifier", {"system": system, "value": value})
