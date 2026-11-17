"""ExplanationOfBenefitParser — pembaca elemen tingkat atas resource FHIR R4 ExplanationOfBenefit.

Dihasilkan dari ExplanationOfBenefitBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class ExplanationOfBenefitParser:
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

    def get_use(self) -> Any:
        return self._data.get("use")

    getUse = get_use

    def get_patient(self) -> Any:
        return self._data.get("patient")

    getPatient = get_patient

    def get_created(self) -> Any:
        return self._data.get("created")

    getCreated = get_created

    def get_provider(self) -> Any:
        return self._data.get("provider")

    getProvider = get_provider
