"""MedicinalProductManufacturedParser — pembaca elemen tingkat atas resource FHIR R4 MedicinalProductManufactured.

Dihasilkan dari MedicinalProductManufacturedBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class MedicinalProductManufacturedParser:
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

    def get_quantity(self) -> Any:
        return self._data.get("quantity")

    getQuantity = get_quantity

    def get_manufacturer(self) -> Any:
        return self._data.get("manufacturer")

    getManufacturer = get_manufacturer

    def get_ingredient(self) -> Any:
        return self._data.get("ingredient")

    getIngredient = get_ingredient
