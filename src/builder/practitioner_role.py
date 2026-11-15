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
        """R4: code 0..* — dulu menimpa, kini menumpuk seperti kanon."""
        return self._append("code", codeable_concept)

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

    def available_time(self, days_of_week: Optional[List[str]] = None, available_start: Optional[str] = None, available_end: Optional[str] = None, description: Optional[str] = None, all_day: Optional[bool] = None) -> "PractitionerRoleBuilder":
        """Kanon menulis `description` di dalam availableTime; R4 tidak punya elemen itu."""
        at: dict = {}
        if days_of_week:
            at["daysOfWeek"] = days_of_week
        if available_start:
            at["availableStartTime"] = available_start
        if available_end:
            at["availableEndTime"] = available_end
        if description is not None:
            at["description"] = description
        if all_day is not None:
            at["allDay"] = all_day
        return self._append("availableTime", at if at else [])

    def not_available(self, description: str, during: Optional[dict] = None) -> "PractitionerRoleBuilder":
        """Dulu menulis `period`; elemen R4 dan kanon adalah `during`."""
        na: dict = {"description": description}
        if during:
            na["during"] = during
        return self._append("notAvailable", na)

    def identifier(self, system: str, value: str) -> "PractitionerRoleBuilder":
        return self._append("identifier", {"system": system, "value": value})

    # --- alias nama kanon -----------------------------------------------------

    def set_id(self, id: str) -> "PractitionerRoleBuilder":
        return self._set("id", id)

    def add_identifier(self, system: str, value: str) -> "PractitionerRoleBuilder":
        return self.identifier(system, value)

    def set_active(self, value: bool) -> "PractitionerRoleBuilder":
        return self.active(value)

    def set_practitioner(self, reference: str, display: Optional[str] = None) -> "PractitionerRoleBuilder":
        return self.practitioner(reference, display)

    def set_organization(self, reference: str, display: Optional[str] = None) -> "PractitionerRoleBuilder":
        return self.organization(reference, display)

    def add_code(self, konsep: dict) -> "PractitionerRoleBuilder":
        return self.code(konsep)

    def add_specialty(self, konsep: dict) -> "PractitionerRoleBuilder":
        return self.specialty(konsep)

    def add_location(self, reference: str, display: Optional[str] = None) -> "PractitionerRoleBuilder":
        return self.location(reference, display)

    def add_healthcare_service(self, reference: str) -> "PractitionerRoleBuilder":
        return self.healthcare_service(reference)

    def add_telecom(self, system: str, value: str, use: Optional[str] = None) -> "PractitionerRoleBuilder":
        return self.telecom(system, value, use)

    def add_available_time(self, days_of_week: Optional[List[str]] = None, available_start: Optional[str] = None, available_end: Optional[str] = None, description: Optional[str] = None) -> "PractitionerRoleBuilder":
        return self.available_time(days_of_week, available_start, available_end, description)

    def add_not_available(self, description: str, during: Optional[dict] = None) -> "PractitionerRoleBuilder":
        return self.not_available(description, during)

    def add_endpoint(self, reference: str) -> "PractitionerRoleBuilder":
        return self.endpoint(reference)

    def set_availability_exceptions(self, text: str) -> "PractitionerRoleBuilder":
        return self._set("availabilityExceptions", text)

    def add_extension(self, url: str, value, value_type: Optional[str] = None) -> "PractitionerRoleBuilder":
        ext = {"url": url}
        if value_type is not None:
            ext[f"value{value_type[0].upper()}{value_type[1:]}"] = value
        else:
            ext["valueString"] = value
        return self._append("extension", ext)

    def add_availability_exceptions(self, text: str) -> "PractitionerRoleBuilder":
        return self.set_availability_exceptions(text)
