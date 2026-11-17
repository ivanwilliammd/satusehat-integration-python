"""ImmunizationRecommendationParser — pembaca elemen tingkat atas resource FHIR R4 ImmunizationRecommendation.

Dihasilkan dari ImmunizationRecommendationBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class ImmunizationRecommendationParser:
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

    def get_code(self) -> Any:
        return self._data.get("code")

    getCode = get_code

    def get_subject(self) -> Any:
        return self._data.get("subject")

    getSubject = get_subject

    def get_description(self) -> Any:
        return self._data.get("description")

    getDescription = get_description

    def get_encounter(self) -> Any:
        return self._data.get("encounter")

    getEncounter = get_encounter

    def get_identifier(self) -> Any:
        return self._data.get("identifier")

    getIdentifier = get_identifier
