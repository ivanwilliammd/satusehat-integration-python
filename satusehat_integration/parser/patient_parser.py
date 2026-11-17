"""PatientParser — parses FHIR Patient resource."""
from __future__ import annotations

from typing import Any, Optional


class PatientParser:
    def __init__(self, patient: Optional[dict[str, Any]] = None) -> None:
        self.patient: dict[str, Any] = patient if isinstance(patient, dict) else {}

    def get_identifiers(self) -> Any:
        return self.patient.get("identifier")

    getIdentifiers = get_identifiers

    def get_name(self) -> Any:
        return self.patient.get("name")

    getName = get_name

    def get_telecom(self) -> Any:
        return self.patient.get("telecom")

    getTelecom = get_telecom

    def get_gender(self) -> Any:
        return self.patient.get("gender")

    getGender = get_gender

    def get_birth_date(self) -> Any:
        return self.patient.get("birthDate")

    getBirthDate = get_birth_date

    def get_deceased(self) -> Any:
        return self.patient.get("deceasedBoolean")

    getDeceased = get_deceased

    def get_address(self) -> Any:
        return self.patient.get("address")

    getAddress = get_address

    def get_marital_status(self) -> Any:
        return self.patient.get("maritalStatus")

    getMaritalStatus = get_marital_status

    def get_multiple_birth(self) -> Any:
        if "multipleBirthBoolean" in self.patient and self.patient["multipleBirthBoolean"] is not None:
            return self.patient["multipleBirthBoolean"]
        return self.patient.get("multipleBirthInteger")

    getMultipleBirth = get_multiple_birth

    def get_emergency_contact(self) -> Any:
        return self.patient.get("contact")

    getEmergencyContact = get_emergency_contact

    def get_communication(self) -> Any:
        return self.patient.get("communication")

    getCommunication = get_communication

    def get_extension(self) -> Any:
        return self.patient.get("extension")

    getExtension = get_extension
