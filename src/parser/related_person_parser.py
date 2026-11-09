"""RelatedPersonParser — parses FHIR RelatedPerson resource."""
from __future__ import annotations

from typing import Any, Optional


class RelatedPersonParser:
    def __init__(self, related_person: Optional[dict[str, Any]] = None) -> None:
        self.related_person: dict[str, Any] = (
            related_person if isinstance(related_person, dict) else {}
        )

    def get_identifiers(self) -> Any:
        return self.related_person.get("identifier")

    getIdentifiers = get_identifiers

    def get_active(self) -> Any:
        return self.related_person.get("active")

    getActive = get_active

    def get_patient_reference(self) -> Optional[str]:
        pat = self.related_person.get("patient")
        return pat.get("reference") if isinstance(pat, dict) else None

    getPatientReference = get_patient_reference

    def get_relationships(self) -> Any:
        return self.related_person.get("relationship")

    getRelationships = get_relationships

    def get_names(self) -> Any:
        return self.related_person.get("name")

    getNames = get_names

    def get_telecoms(self) -> Any:
        return self.related_person.get("telecom")

    getTelecoms = get_telecoms

    def get_gender(self) -> Any:
        return self.related_person.get("gender")

    getGender = get_gender

    def get_birth_date(self) -> Any:
        return self.related_person.get("birthDate")

    getBirthDate = get_birth_date

    def get_addresses(self) -> Any:
        return self.related_person.get("address")

    getAddresses = get_addresses

    def get_communications(self) -> Any:
        return self.related_person.get("communication")

    getCommunications = get_communications
