"""ChargeItemParser — typed accessors over the official SATUSEHAT ChargeItem payload.

Shape source: satusehat-conformance/examples/satusehat/ChargeItem.json, copied unchanged to
satusehat_integration/parser/testdata/ChargeItem.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class ChargeItemParser:
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

    def get_code(self) -> Any:
        return self.payload.get("code")

    getCode = get_code

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_context(self) -> Any:
        return self.payload.get("context")

    getContext = get_context

    def get_occurrence_period(self) -> Any:
        return self.payload.get("occurrencePeriod")

    getOccurrencePeriod = get_occurrence_period

    def get_performer(self) -> Any:
        return self.payload.get("performer")

    getPerformer = get_performer

    def get_quantity(self) -> Any:
        return self.payload.get("quantity")

    getQuantity = get_quantity

    def get_account(self) -> Any:
        return self.payload.get("account")

    getAccount = get_account

    def get_extension(self) -> Any:
        return self.payload.get("extension")

    getExtension = get_extension
