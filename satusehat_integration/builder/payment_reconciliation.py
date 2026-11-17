from typing import Any, Dict, List, Optional

from satusehat_integration.builder.base_builder import BaseBuilder


class PaymentReconciliationBuilder(BaseBuilder):
    """Setara PayloadBuilderPaymentReconciliation.php.

    Versi sebelumnya hanya punya enam method tanpa awalan `set_`, dua di antaranya
    menulis elemen yang salah (`periodEnd`, `outcome` sebagai string). Ditulis ulang
    mengikuti PHP; nama lama dipertahankan sebagai alias supaya pemanggil tidak rusak.
    """

    def __init__(self) -> None:
        super().__init__("PaymentReconciliation")

    # --- inti -----------------------------------------------------------------

    def set_id(self, id: str) -> "PaymentReconciliationBuilder":
        return self._set("id", id)

    def add_identifier(self, system: str, value: str) -> "PaymentReconciliationBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_status(self, status: str) -> "PaymentReconciliationBuilder":
        return self._set("status", status)

    def set_type(self, system: str, code: str, display: str = "") -> "PaymentReconciliationBuilder":
        return self._set("type", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_created(self, created: str) -> "PaymentReconciliationBuilder":
        return self._set("created", created)

    def set_period(self, start: str, end: str = "") -> "PaymentReconciliationBuilder":
        self._set("period", {"start": start})
        if end:
            self.data["period"]["end"] = end
        return self

    def set_request(self, reference: str) -> "PaymentReconciliationBuilder":
        return self._set("request", {"reference": reference})

    def set_request_provider(self, reference: str) -> "PaymentReconciliationBuilder":
        return self._set("requestProvider", {"reference": reference})

    def set_outcome(self, system: str, code: str, display: str = "") -> "PaymentReconciliationBuilder":
        return self._set("outcome", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_disposition(self, disposition: str) -> "PaymentReconciliationBuilder":
        return self._set("disposition", disposition)

    def set_insurer(self, reference: str) -> "PaymentReconciliationBuilder":
        return self._set("insurer", {"reference": reference})

    def set_request_match_date(self, date: str) -> "PaymentReconciliationBuilder":
        return self._set("requestMatchDate", date)

    def set_outcome_code(self, system: str, code: str, display: str = "") -> "PaymentReconciliationBuilder":
        return self._push("outcomeCode", {"coding": [{"system": system, "code": code, "display": display}]})

    def add_requestor(self, reference: str, display: str = "") -> "PaymentReconciliationBuilder":
        requestor: Dict[str, Any] = {"reference": reference}
        if display:
            requestor["display"] = display
        return self._push("requestor", requestor)

    def add_process_note(self, text: str, type: Optional[str] = None) -> "PaymentReconciliationBuilder":
        note: Dict[str, Any] = {"text": text}
        if type:
            note["type"] = type
        return self._push("processNote", note)

    # --- pembayaran ----------------------------------------------------------

    def set_payment_date(self, date: str) -> "PaymentReconciliationBuilder":
        return self._set("paymentDate", date)

    def set_payment_amount(self, value: float, code: str = "IDR") -> "PaymentReconciliationBuilder":
        self._set("paymentAmount", {"value": value, "currency": code})
        return self

    def set_payment_identifier(self, system: str, value: str) -> "PaymentReconciliationBuilder":
        return self._set("paymentIdentifier", {"system": system, "value": value})

    def add_detail(
        self,
        type_system: str,
        type_code: str,
        amount: Optional[float] = None,
        request_reference: Optional[str] = None,
    ) -> "PaymentReconciliationBuilder":
        detail: Dict[str, Any] = {"type": {"coding": [{"system": type_system, "code": type_code}]}}
        if amount is not None:
            detail["amount"] = {"value": amount}
        if request_reference:
            detail["request"] = {"reference": request_reference}
        return self._push("detail", detail)

    def set_total_amount(self, value: float, code: str = "IDR") -> "PaymentReconciliationBuilder":
        self._set("totalAmount", {"value": value, "currency": code})
        return self

    # --- alias nama lama ------------------------------------------------------

    def status(self, value: str) -> "PaymentReconciliationBuilder":
        return self.set_status(value)

    def created(self, value: str) -> "PaymentReconciliationBuilder":
        return self.set_created(value)

    def period_start(self, value: str) -> "PaymentReconciliationBuilder":
        period = self.data.get("period") or {}
        period["start"] = value
        return self._set("period", period)

    def period_end(self, value: str) -> "PaymentReconciliationBuilder":
        period = self.data.get("period") or {}
        period["end"] = value
        return self._set("period", period)

    def requestor(self, reference: str) -> "PaymentReconciliationBuilder":
        return self.add_requestor(reference)

    def outcome(self, value: str) -> "PaymentReconciliationBuilder":
        """Dulu menulis `outcome` sebagai string. Kini tidak: nama ini ambigu.

        Pemanggil yang butuh string harus memakai set_outcome(system, code) —
        `outcome` di R4 bertipe CodeableConcept, bukan string.
        """
        return self._set("outcome", {"text": value})
