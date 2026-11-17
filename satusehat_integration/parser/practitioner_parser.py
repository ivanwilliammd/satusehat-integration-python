"""PractitionerParser — parses FHIR Practitioner resource."""
from __future__ import annotations

from typing import Any, Optional

from ..ssrequest.oauth2_client import OAuth2Client


class PractitionerParser(OAuth2Client):
    def __init__(self, practitioner: Optional[dict[str, Any]] = None) -> None:
        # Do not call super().__init__() eagerly so offline dict parsing works without env vars
        self.practitioner: Optional[dict[str, Any]] = (
            practitioner if isinstance(practitioner, dict) else None
        )

    def get_ss_nik(self, nik: str) -> Optional[dict[str, Any]]:
        if not hasattr(self, "fhir_url"):
            super().__init__()
        status_code, res = self.get_by_nik("Practitioner", nik)
        if status_code != 200 or not isinstance(res, dict):
            return None
        entries = res.get("entry")
        if isinstance(entries, list) and entries and isinstance(entries[0], dict):
            self.practitioner = entries[0].get("resource")
        else:
            self.practitioner = None
        return self.practitioner

    getSSNik = get_ss_nik

    def get_id(self) -> Optional[str]:
        if not self.practitioner:
            return None
        return self.practitioner.get("id")

    getId = get_id

    def get_identifiers(self) -> Any:
        return self.practitioner.get("identifier") if self.practitioner else None

    getIdentifiers = get_identifiers

    def get_active(self) -> Any:
        return self.practitioner.get("active") if self.practitioner else None

    getActive = get_active

    def get_name(self) -> Any:
        return self.practitioner.get("name") if self.practitioner else None

    getName = get_name

    def get_telecom(self) -> Any:
        return self.practitioner.get("telecom") if self.practitioner else None

    getTelecom = get_telecom

    def get_address(self) -> Any:
        return self.practitioner.get("address") if self.practitioner else None

    getAddress = get_address

    def get_address_line(self) -> Any:
        if not self.practitioner:
            return None
        addresses = self.practitioner.get("address")
        if isinstance(addresses, list) and addresses and isinstance(addresses[0], dict):
            lines = addresses[0].get("line")
            if isinstance(lines, list) and lines:
                return lines[0]
        return None

    getAddressLine = get_address_line

    def get_city(self) -> Any:
        if not self.practitioner:
            return None
        addresses = self.practitioner.get("address")
        if isinstance(addresses, list) and addresses and isinstance(addresses[0], dict):
            exts = addresses[0].get("extension")
            if isinstance(exts, list) and exts and isinstance(exts[0], dict):
                sub_exts = exts[0].get("extension")
                if isinstance(sub_exts, list) and len(sub_exts) > 1 and isinstance(sub_exts[1], dict):
                    return sub_exts[1].get("valueCode")
        return None

    getCity = get_city

    def get_village(self) -> Any:
        if not self.practitioner:
            return None
        addresses = self.practitioner.get("address")
        if isinstance(addresses, list) and addresses and isinstance(addresses[0], dict):
            exts = addresses[0].get("extension")
            if isinstance(exts, list) and exts and isinstance(exts[0], dict):
                sub_exts = exts[0].get("extension")
                if isinstance(sub_exts, list) and len(sub_exts) > 3 and isinstance(sub_exts[3], dict):
                    return sub_exts[3].get("valueCode")
        return None

    getVillage = get_village

    def get_gender(self) -> Any:
        return self.practitioner.get("gender") if self.practitioner else None

    getGender = get_gender

    def get_birth_date(self) -> Any:
        return self.practitioner.get("birthDate") if self.practitioner else None

    getBirthDate = get_birth_date

    def get_photo(self) -> Any:
        return self.practitioner.get("photo") if self.practitioner else None

    getPhoto = get_photo

    def get_qualifications(self) -> Any:
        if not self.practitioner:
            return None
        quals = self.practitioner.get("qualification")
        if isinstance(quals, list) and quals and isinstance(quals[0], dict):
            idents = quals[0].get("identifier")
            if isinstance(idents, list) and idents and isinstance(idents[0], dict):
                return idents[0].get("value")
        return None

    getQualifications = get_qualifications

    def get_communication(self) -> Any:
        return self.practitioner.get("communication") if self.practitioner else None

    getCommunication = get_communication
