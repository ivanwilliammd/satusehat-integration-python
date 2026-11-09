"""OrganizationParser — parses FHIR Organization resource."""
from __future__ import annotations

from typing import Any, Optional


def _remove_prefix(value: Optional[str], prefix: str) -> Optional[str]:
    if value and isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class OrganizationParser:
    def __init__(self, organization: Optional[dict[str, Any]] = None) -> None:
        self.organization: dict[str, Any] = organization if isinstance(organization, dict) else {}

    def get_identifiers(self) -> Any:
        return self.organization.get("identifier")

    getIdentifiers = get_identifiers

    def get_name(self) -> Any:
        return self.organization.get("name")

    getName = get_name

    def get_operational_status(self) -> Any:
        return self.organization.get("extension")

    getOperationalStatus = get_operational_status

    def get_part_of(self) -> Any:
        return self.organization.get("partOf")

    getPartOf = get_part_of

    def get_part_of_reference(self) -> Optional[str]:
        part = self.organization.get("partOf")
        ref = part.get("reference") if isinstance(part, dict) else None
        return _remove_prefix(ref, "Organization/")

    getPartOfReference = get_part_of_reference

    def get_type(self) -> Any:
        return self.organization.get("type")

    getType = get_type

    def get_telecom(self) -> Any:
        return self.organization.get("telecom")

    getTelecom = get_telecom

    def get_address(self) -> Any:
        return self.organization.get("address")

    getAddress = get_address
