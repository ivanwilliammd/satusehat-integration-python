from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class PractitionerRoleBuilder(BaseBuilder):
    _resourceType = "PractitionerRole"

    def __init__(self) -> None:
        super().__init__("PractitionerRole")

    def active(self, value: bool) -> "PractitionerRoleBuilder":
        return self._set("active", value)

    def practitioner(self, reference: str, display: Optional[str] = None) -> "PractitionerRoleBuilder":
        pr: dict = {"reference": reference}
        if display:
            pr["display"] = display
        return self._set("practitioner", pr)

    def organization(self, reference: str, display: Optional[str] = None) -> "PractitionerRoleBuilder":
        org: dict = {"reference": reference}
        if display:
            org["display"] = display
        return self._set("organization", org)

    def code(self, codeable_concept: dict) -> "PractitionerRoleBuilder":
        return self._set("code", [codeable_concept])

    def specialty(self, codeable_concept: dict) -> "PractitionerRoleBuilder":
        return self._append("specialty", codeable_concept)

    def location(self, reference: str, display: Optional[str] = None) -> "PractitionerRoleBuilder":
        loc: dict = {"reference": reference}
        if display:
            loc["display"] = display
        return self._append("location", loc)

    def healthcare_service(self, reference: str) -> "PractitionerRoleBuilder":
        return self._append("healthcareService", {"reference": reference})

    def telecom(self, system: str, value: str, use: Optional[str] = None) -> "PractitionerRoleBuilder":
        tc: dict = {"system": system, "value": value}
        if use:
            tc["use"] = use
        return self._append("telecom", tc)

    def endpoint(self, reference: str) -> "PractitionerRoleBuilder":
        return self._append("endpoint", {"reference": reference})

    def available_time(self, days_of_week: Optional[List[str]] = None, available_start: Optional[str] = None, available_end: Optional[str] = None, all_day: Optional[bool] = None) -> "PractitionerRoleBuilder":
        at: dict = {}
        if days_of_week:
            at["daysOfWeek"] = days_of_week
        if available_start:
            at["availableStartTime"] = available_start
        if available_end:
            at["availableEndTime"] = available_end
        if all_day is not None:
            at["allDay"] = all_day
        return self._append("availableTime", at) if at else self

    def not_available(self, description: str, period: Optional[dict] = None) -> "PractitionerRoleBuilder":
        na: dict = {"description": description}
        if period:
            na["period"] = period
        return self._append("notAvailable", na)

    def identifier(self, system: str, value: str) -> "PractitionerRoleBuilder":
        return self._append("identifier", {"system": system, "value": value})
