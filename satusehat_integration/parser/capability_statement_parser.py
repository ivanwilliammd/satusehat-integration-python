"""CapabilityStatementParser — pembaca elemen tingkat atas resource FHIR R4 CapabilityStatement.

Dihasilkan dari CapabilityStatementBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class CapabilityStatementParser:
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

    def get_date(self) -> Any:
        return self._data.get("date")

    getDate = get_date

    def get_kind(self) -> Any:
        return self._data.get("kind")

    getKind = get_kind

    def get_fhir_version(self) -> Any:
        return self._data.get("fhirVersion")

    getFhirVersion = get_fhir_version

    def get_format(self) -> Any:
        return self._data.get("format")

    getFormat = get_format

    def get_rest(self) -> Any:
        return self._data.get("rest")

    getRest = get_rest
