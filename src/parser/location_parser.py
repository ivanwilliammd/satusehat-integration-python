"""LocationParser — parses FHIR Location resource."""
from __future__ import annotations

from typing import Any, Optional


def _remove_prefix(value: Optional[str], prefix: str) -> Optional[str]:
    if value and isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class LocationParser:
    def __init__(self, location: Optional[dict[str, Any]] = None) -> None:
        self.location: dict[str, Any] = location if isinstance(location, dict) else {}

    def get_identifiers(self) -> Any:
        return self.location.get("identifier")

    getIdentifiers = get_identifiers

    def get_name(self) -> Any:
        return self.location.get("name")

    getName = get_name

    def get_status(self) -> Any:
        return self.location.get("status")

    getStatus = get_status

    def get_operational_status(self) -> Any:
        return self.location.get("operationalStatus")

    getOperationalStatus = get_operational_status

    def get_telecom(self) -> Any:
        return self.location.get("telecom")

    getTelecom = get_telecom

    def get_address(self) -> Any:
        return self.location.get("address")

    getAddress = get_address

    def get_physical_type(self) -> Any:
        return self.location.get("physicalType")

    getPhysicalType = get_physical_type

    def get_position(self) -> Any:
        return self.location.get("position")

    getPosition = get_position

    def get_managing_organization(self) -> Any:
        return self.location.get("managingOrganization")

    getManagingOrganization = get_managing_organization

    def get_managing_organization_reference(self) -> Optional[str]:
        org = self.location.get("managingOrganization")
        ref = org.get("reference") if isinstance(org, dict) else None
        return _remove_prefix(ref, "Organization/")

    getManagingOrganizationReference = get_managing_organization_reference

    def get_part_of(self) -> Any:
        return self.location.get("partOf")

    getPartOf = get_part_of

    def get_part_of_reference(self) -> Optional[str]:
        part = self.location.get("partOf")
        ref = part.get("reference") if isinstance(part, dict) else None
        return _remove_prefix(ref, "Location/")

    getPartOfReference = get_part_of_reference
