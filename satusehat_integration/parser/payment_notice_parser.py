"""PaymentNoticeParser — typed accessors over the official SATUSEHAT PaymentNotice payload.

Shape source: satusehat-conformance/examples/satusehat/PaymentNotice.json, copied unchanged to
satusehat_integration/parser/testdata/PaymentNotice.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class PaymentNoticeParser:
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

    def get_request(self) -> Any:
        return self.payload.get("request")

    getRequest = get_request

    def get_response(self) -> Any:
        return self.payload.get("response")

    getResponse = get_response

    def get_created(self) -> Any:
        return self.payload.get("created")

    getCreated = get_created

    def get_payment_date(self) -> Any:
        return self.payload.get("paymentDate")

    getPaymentDate = get_payment_date

    def get_provider(self) -> Any:
        return self.payload.get("provider")

    getProvider = get_provider

    def get_payee(self) -> Any:
        return self.payload.get("payee")

    getPayee = get_payee

    def get_recipient(self) -> Any:
        return self.payload.get("recipient")

    getRecipient = get_recipient

    def get_amount(self) -> Any:
        return self.payload.get("amount")

    getAmount = get_amount

    def get_payment(self) -> Any:
        return self.payload.get("payment")

    getPayment = get_payment

    def get_payment_status(self) -> Any:
        return self.payload.get("paymentStatus")

    getPaymentStatus = get_payment_status
