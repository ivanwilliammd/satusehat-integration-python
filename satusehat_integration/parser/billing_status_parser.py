"""BillingStatusParser — typed accessors over the official SATUSEHAT BillingStatus payload.

Shape source: satusehat-conformance/examples/satusehat/BillingStatus.json, copied unchanged to
satusehat_integration/parser/testdata/BillingStatus.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class BillingStatusParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_id(self) -> Any:
        return self.payload.get("id")

    getId = get_id

    def get_identifier(self) -> Any:
        return self.payload.get("identifier")

    getIdentifier = get_identifier

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_insurer(self) -> Any:
        return self.payload.get("insurer")

    getInsurer = get_insurer

    def get_recipient(self) -> Any:
        return self.payload.get("recipient")

    getRecipient = get_recipient

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_request(self) -> Any:
        return self.payload.get("request")

    getRequest = get_request
