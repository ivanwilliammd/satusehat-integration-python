"""PaymentReconciliationParser — typed accessors over the official SATUSEHAT PaymentReconciliation payload.

Shape source: satusehat-conformance/examples/satusehat/PaymentReconciliation.json, copied unchanged to
satusehat_integration/parser/testdata/PaymentReconciliation.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class PaymentReconciliationParser:
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

    def get_period(self) -> Any:
        return self.payload.get("period")

    getPeriod = get_period

    def get_created(self) -> Any:
        return self.payload.get("created")

    getCreated = get_created

    def get_payment_issuer(self) -> Any:
        return self.payload.get("paymentIssuer")

    getPaymentIssuer = get_payment_issuer

    def get_requestor(self) -> Any:
        return self.payload.get("requestor")

    getRequestor = get_requestor

    def get_outcome(self) -> Any:
        return self.payload.get("outcome")

    getOutcome = get_outcome

    def get_disposition(self) -> Any:
        return self.payload.get("disposition")

    getDisposition = get_disposition

    def get_payment_date(self) -> Any:
        return self.payload.get("paymentDate")

    getPaymentDate = get_payment_date

    def get_payment_amount(self) -> Any:
        return self.payload.get("paymentAmount")

    getPaymentAmount = get_payment_amount

    def get_detail(self) -> Any:
        return self.payload.get("detail")

    getDetail = get_detail

    def get_process_note(self) -> Any:
        return self.payload.get("processNote")

    getProcessNote = get_process_note

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_type(self) -> Any:
        return self._data.get("type")

    getType = get_type

    def get_request(self) -> Any:
        return self._data.get("request")

    getRequest = get_request

    def get_request_provider(self) -> Any:
        return self._data.get("requestProvider")

    getRequestProvider = get_request_provider

    def get_insurer(self) -> Any:
        return self._data.get("insurer")

    getInsurer = get_insurer

    def get_request_match_date(self) -> Any:
        return self._data.get("requestMatchDate")

    getRequestMatchDate = get_request_match_date

    def get_payment_identifier(self) -> Any:
        return self._data.get("paymentIdentifier")

    getPaymentIdentifier = get_payment_identifier

    def get_total_amount(self) -> Any:
        return self._data.get("totalAmount")

    getTotalAmount = get_total_amount
