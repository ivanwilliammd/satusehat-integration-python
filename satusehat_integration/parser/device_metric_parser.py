"""DeviceMetricParser — pembaca elemen tingkat atas resource FHIR R4 DeviceMetric.

Dihasilkan dari DeviceMetricBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class DeviceMetricParser:
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

    def get_category(self) -> Any:
        return self._data.get("category")

    getCategory = get_category

    def get_measurement_period(self) -> Any:
        return self._data.get("measurementPeriod")

    getMeasurementPeriod = get_measurement_period
