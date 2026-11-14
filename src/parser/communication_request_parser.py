"""CommunicationRequestParser — typed accessors over the official SATUSEHAT CommunicationRequest payload.

Shape source: satusehat-conformance/examples/satusehat/CommunicationRequest.json, copied unchanged to
src/parser/testdata/CommunicationRequest.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class CommunicationRequestParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_category(self) -> Any:
        return self.payload.get("category")

    getCategory = get_category

    def get_payload(self) -> Any:
        return self.payload.get("payload")

    getPayload = get_payload

    def get_about(self) -> Any:
        return self.payload.get("about")

    getAbout = get_about

    def get_sender(self) -> Any:
        return self.payload.get("sender")

    getSender = get_sender

    def get_recipient(self) -> Any:
        return self.payload.get("recipient")

    getRecipient = get_recipient
