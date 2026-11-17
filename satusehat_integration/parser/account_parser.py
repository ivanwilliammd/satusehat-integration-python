"""AccountParser — typed accessors over the official SATUSEHAT Account payload.

Shape source: satusehat-conformance/examples/satusehat/Account.json, copied unchanged to
satusehat_integration/parser/testdata/Account.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class AccountParser:
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

    def get_type(self) -> Any:
        return self.payload.get("type")

    getType = get_type

    def get_name(self) -> Any:
        return self.payload.get("name")

    getName = get_name

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_service_period(self) -> Any:
        return self.payload.get("servicePeriod")

    getServicePeriod = get_service_period

    def get_owner(self) -> Any:
        return self.payload.get("owner")

    getOwner = get_owner

    def get_guarantor(self) -> Any:
        return self.payload.get("guarantor")

    getGuarantor = get_guarantor

    def get_description(self) -> Any:
        return self.payload.get("description")

    getDescription = get_description
