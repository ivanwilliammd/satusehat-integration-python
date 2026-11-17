"""CatalogEntryParser — pembaca elemen tingkat atas resource FHIR R4 CatalogEntry.

Dihasilkan dari CatalogEntryBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class CatalogEntryParser:
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

    def get_type(self) -> Any:
        return self._data.get("type")

    getType = get_type

    def get_reference(self) -> Any:
        return self._data.get("reference")

    getReference = get_reference

    def get_validity_period(self) -> Any:
        return self._data.get("validityPeriod")

    getValidityPeriod = get_validity_period
