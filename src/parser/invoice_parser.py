"""InvoiceParser — typed accessors over the official SATUSEHAT Invoice payload.

Shape source: satusehat-conformance/examples/satusehat/Invoice.json, copied unchanged to
src/parser/testdata/Invoice.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class InvoiceParser:
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

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_date(self) -> Any:
        return self.payload.get("date")

    getDate = get_date

    def get_issuer(self) -> Any:
        return self.payload.get("issuer")

    getIssuer = get_issuer

    def get_account(self) -> Any:
        return self.payload.get("account")

    getAccount = get_account

    def get_line_item(self) -> Any:
        return self.payload.get("lineItem")

    getLineItem = get_line_item

    def get_total_net(self) -> Any:
        return self.payload.get("totalNet")

    getTotalNet = get_total_net
