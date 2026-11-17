"""ResourceGuideParser — pembaca elemen tingkat atas resource FHIR R4 ResourceGuide.

Dihasilkan dari ResourceGuideBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class ResourceGuideParser:
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

    def get_name(self) -> Any:
        return self._data.get("name")

    getName = get_name

    def get_description(self) -> Any:
        return self._data.get("description")

    getDescription = get_description

    def get_version(self) -> Any:
        return self._data.get("version")

    getVersion = get_version

    def get_publisher(self) -> Any:
        return self._data.get("publisher")

    getPublisher = get_publisher
