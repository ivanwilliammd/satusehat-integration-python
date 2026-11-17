"""EnrollmentResponseParser — pembaca elemen tingkat atas resource FHIR R4 EnrollmentResponse.

Dihasilkan dari EnrollmentResponseBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class EnrollmentResponseParser:
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

    def get_request(self) -> Any:
        return self._data.get("request")

    getRequest = get_request

    def get_outcome(self) -> Any:
        return self._data.get("outcome")

    getOutcome = get_outcome

    def get_disposition(self) -> Any:
        return self._data.get("disposition")

    getDisposition = get_disposition

    def get_created(self) -> Any:
        return self._data.get("created")

    getCreated = get_created
