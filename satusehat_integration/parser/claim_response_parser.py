"""ClaimResponseParser — typed accessors over the official SATUSEHAT ClaimResponse payload.

Shape source: satusehat-conformance/examples/satusehat/ClaimResponse.json, copied unchanged to
satusehat_integration/parser/testdata/ClaimResponse.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class ClaimResponseParser:
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

    def get_identifier(self) -> Any:
        return self.payload.get("identifier")

    getIdentifier = get_identifier

    def get_type(self) -> Any:
        return self.payload.get("type")

    getType = get_type

    def get_use(self) -> Any:
        return self.payload.get("use")

    getUse = get_use

    def get_patient(self) -> Any:
        return self.payload.get("patient")

    getPatient = get_patient

    def get_created(self) -> Any:
        return self.payload.get("created")

    getCreated = get_created

    def get_insurer(self) -> Any:
        return self.payload.get("insurer")

    getInsurer = get_insurer

    def get_requestor(self) -> Any:
        return self.payload.get("requestor")

    getRequestor = get_requestor

    def get_request(self) -> Any:
        return self.payload.get("request")

    getRequest = get_request

    def get_outcome(self) -> Any:
        return self.payload.get("outcome")

    getOutcome = get_outcome

    def get_payee_type(self) -> Any:
        return self.payload.get("payeeType")

    getPayeeType = get_payee_type

    def get_adjudication(self) -> Any:
        return self.payload.get("adjudication")

    getAdjudication = get_adjudication

    def get_item(self) -> Any:
        return self.payload.get("item")

    getItem = get_item

    def get_total(self) -> Any:
        return self.payload.get("total")

    getTotal = get_total

    def get_payment(self) -> Any:
        return self.payload.get("payment")

    getPayment = get_payment
