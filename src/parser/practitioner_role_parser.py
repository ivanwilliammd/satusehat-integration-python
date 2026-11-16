"""PractitionerRoleParser — pembaca elemen tingkat atas resource FHIR R4 PractitionerRole.

Dihasilkan dari PractitionerRoleBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class PractitionerRoleParser:
    def __init__(self, data: Optional[dict[str, Any]] = None) -> None:
        self._data: dict[str, Any] = data if isinstance(data, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self._data

    getRaw = get_raw

    def get_active(self) -> Any:
        return self._data.get("active")

    getActive = get_active

    def get_practitioner(self) -> Any:
        return self._data.get("practitioner")

    getPractitioner = get_practitioner

    def get_organization(self) -> Any:
        return self._data.get("organization")

    getOrganization = get_organization

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_availability_exceptions(self) -> Any:
        return self._data.get("availabilityExceptions")

    getAvailabilityExceptions = get_availability_exceptions

    def get_code(self) -> Any:
        return self._data.get("code")

    getCode = get_code

    def get_specialty(self) -> Any:
        return self._data.get("specialty")

    getSpecialty = get_specialty

    def get_location(self) -> Any:
        return self._data.get("location")

    getLocation = get_location

    def get_healthcare_service(self) -> Any:
        return self._data.get("healthcareService")

    getHealthcareService = get_healthcare_service

    def get_telecom(self) -> Any:
        return self._data.get("telecom")

    getTelecom = get_telecom

    def get_endpoint(self) -> Any:
        return self._data.get("endpoint")

    getEndpoint = get_endpoint

    def get_available_time(self) -> Any:
        return self._data.get("availableTime")

    getAvailableTime = get_available_time

    def get_not_available(self) -> Any:
        return self._data.get("notAvailable")

    getNotAvailable = get_not_available

    def get_identifier(self) -> Any:
        return self._data.get("identifier")

    getIdentifier = get_identifier

    def get_extension(self) -> Any:
        return self._data.get("extension")

    getExtension = get_extension
