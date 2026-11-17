"""EndpointParser — pembaca elemen tingkat atas resource FHIR R4 Endpoint.

Dihasilkan dari EndpointBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class EndpointParser:
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

    def get_connection_type(self) -> Any:
        return self._data.get("connectionType")

    getConnectionType = get_connection_type

    def get_name(self) -> Any:
        return self._data.get("name")

    getName = get_name

    def get_managing_organization(self) -> Any:
        return self._data.get("managingOrganization")

    getManagingOrganization = get_managing_organization

    def get_period(self) -> Any:
        return self._data.get("period")

    getPeriod = get_period

    def get_address(self) -> Any:
        return self._data.get("address")

    getAddress = get_address

    def get_identifier(self) -> Any:
        return self._data.get("identifier")

    getIdentifier = get_identifier

    def get_contact(self) -> Any:
        return self._data.get("contact")

    getContact = get_contact

    def get_payload_type(self) -> Any:
        return self._data.get("payloadType")

    getPayloadType = get_payload_type

    def get_payload_mime_type(self) -> Any:
        return self._data.get("payloadMimeType")

    getPayloadMimeType = get_payload_mime_type

    def get_header(self) -> Any:
        return self._data.get("header")

    getHeader = get_header
