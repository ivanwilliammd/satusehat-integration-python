"""MedicinalProductAuthorizationParser — pembaca elemen tingkat atas resource FHIR R4 MedicinalProductAuthorization.

Dihasilkan dari MedicinalProductAuthorizationBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class MedicinalProductAuthorizationParser:
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

    def get_country(self) -> Any:
        return self._data.get("country")

    getCountry = get_country

    def get_regulator(self) -> Any:
        return self._data.get("regulator")

    getRegulator = get_regulator

    def get_validity_period(self) -> Any:
        return self._data.get("validityPeriod")

    getValidityPeriod = get_validity_period
