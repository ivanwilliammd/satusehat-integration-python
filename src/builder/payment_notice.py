"""PaymentNotice resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderPaymentNotice.php. Versi sebelumnya enam method tanpa awalan
`set_`, dan `amount` menulis Money langsung — yang benar menurut R4, tetapi bukan
yang ditulis kanon.

Tiga quirk PHP ditiru dan ditandai (lihat docs/R4_CONFORMANCE_AUDIT.md):
- setPayment(value, code) menulis `payment/amount/value` dan `payment/amount/currency`,
  padahal PaymentNotice.payment bertipe Reference dan Money tinggal di `amount`;
- setInsurer menulis `insurer`, yang tidak ada di PaymentNotice R4;
- setPaymentReconciliation menulis `paymentReconciliation`, yang juga tidak ada;
  elemen R4-nya `payment`.
"""
from typing import Any, Dict

from src.builder.base_builder import BaseBuilder


class PaymentNoticeBuilder(BaseBuilder):
    """Builder for PaymentNotice resource."""

    def __init__(self) -> None:
        super().__init__("PaymentNotice")

    def _push(self, key: str, value: Any) -> "PaymentNoticeBuilder":  # type: ignore[override]
        self.data.setdefault(key, []).append(value)
        return self

    def _set_path(self, path: str, value: Any) -> "PaymentNoticeBuilder":
        segs = path.split("/")
        cur: Any = self.data
        for seg in segs[:-1]:
            cur = cur.setdefault(seg, {})
        cur[segs[-1]] = value
        return self

    def set_id(self, id: str) -> "PaymentNoticeBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, system: str, value: str) -> "PaymentNoticeBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_status(self, status: str) -> "PaymentNoticeBuilder":
        self.data["status"] = status
        return self

    def set_request(self, reference: str) -> "PaymentNoticeBuilder":
        self.data["request"] = {"reference": reference}
        return self

    def set_response(self, reference: str) -> "PaymentNoticeBuilder":
        self.data["response"] = {"reference": reference}
        return self

    def set_status_date(self, date: str) -> "PaymentNoticeBuilder":
        self.data["statusDate"] = date
        return self

    def set_created(self, created: str) -> "PaymentNoticeBuilder":
        self.data["created"] = created
        return self

    def set_provider(self, reference: str) -> "PaymentNoticeBuilder":
        self.data["provider"] = {"reference": reference}
        return self

    def set_payee(self, reference: str) -> "PaymentNoticeBuilder":
        self.data["payee"] = {"reference": reference}
        return self

    def set_payment(self, value: float, code: str = "IDR") -> "PaymentNoticeBuilder":
        """Quirk PHP: `payment` di R4 adalah Reference, Money tinggal di `amount`."""
        self._set_path("payment/amount/value", value)
        self._set_path("payment/amount/currency", code)
        return self

    def set_payment_date(self, date: str) -> "PaymentNoticeBuilder":
        self.data["paymentDate"] = date
        return self

    def set_payment_status(self, system: str, code: str, display: str = "") -> "PaymentNoticeBuilder":
        self.data["paymentStatus"] = {"coding": [{"system": system, "code": code, "display": display}]}
        return self

    def set_insurer(self, reference: str) -> "PaymentNoticeBuilder":
        """Quirk PHP: `insurer` tidak ada di PaymentNotice R4."""
        self.data["insurer"] = {"reference": reference}
        return self

    def set_payment_reconciliation(self, reference: str) -> "PaymentNoticeBuilder":
        """Quirk PHP: elemen R4-nya `payment`, bukan `paymentReconciliation`."""
        self.data["paymentReconciliation"] = {"reference": reference}
        return self

    # --- alias nama lama ------------------------------------------------------

    def status(self, value: str) -> "PaymentNoticeBuilder":
        return self.set_status(value)

    def request(self, reference: str) -> "PaymentNoticeBuilder":
        return self.set_request(reference)

    def response(self, reference: str) -> "PaymentNoticeBuilder":
        return self.set_response(reference)

    def created(self, value: str) -> "PaymentNoticeBuilder":
        return self.set_created(value)

    def provider(self, reference: str) -> "PaymentNoticeBuilder":
        return self.set_provider(reference)

    def amount(self, value: float, code: str = "IDR") -> "PaymentNoticeBuilder":
        """Tambahan yang sah R4 dan tidak ada di kanon: Money langsung di `amount`."""
        self.data["amount"] = {"value": value, "currency": code}
        return self
