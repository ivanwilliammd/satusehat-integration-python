"""PurificationDecisionParser — pembaca elemen tingkat atas resource FHIR R4 PurificationDecision.

Dihasilkan dari PurificationDecisionBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class PurificationDecisionParser:
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

    def get_insurer(self) -> Any:
        return self._data.get("insurer")

    getInsurer = get_insurer

    def get_provider(self) -> Any:
        return self._data.get("provider")

    getProvider = get_provider

    def get_claim_response(self) -> Any:
        return self._data.get("claimResponse")

    getClaimResponse = get_claim_response

    def get_created(self) -> Any:
        return self._data.get("created")

    getCreated = get_created

    def get_identifier(self) -> Any:
        return self._data.get("identifier")

    getIdentifier = get_identifier
