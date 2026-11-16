"""OrganizationAffiliationParser — pembaca elemen tingkat atas resource FHIR R4 OrganizationAffiliation.

Dihasilkan dari OrganizationAffiliationBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class OrganizationAffiliationParser:
    def __init__(self, data: Optional[dict[str, Any]] = None) -> None:
        self._data: dict[str, Any] = data if isinstance(data, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self._data

    getRaw = get_raw

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_status(self) -> Any:
        return self._data.get("status")

    getStatus = get_status

    def get_organization(self) -> Any:
        return self._data.get("organization")

    getOrganization = get_organization

    def get_participating_organization(self) -> Any:
        return self._data.get("participatingOrganization")

    getParticipatingOrganization = get_participating_organization

    def get_network(self) -> Any:
        return self._data.get("network")

    getNetwork = get_network

    def get_code(self) -> Any:
        return self._data.get("code")

    getCode = get_code
