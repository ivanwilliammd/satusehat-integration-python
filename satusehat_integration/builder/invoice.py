"""Invoice resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderInvoice.php. Versi sebelumnya berbeda pada enam hal yang
membuat payload tidak bisa dibandingkan:

- `set_code` menulis `code`, padahal R4 dan kanon memakai `type`;
- `add_line_item` memakai urutan (sequence, code, system) dan menulis `sequence`
  sebagai string; kanon (sequence, system, code, display, quantity, unitPrice,
  priceFactor) dan menulis angka;
- `add_line_item_price_component` menulis `code` sebagai CodeableConcept dan
  `value`, padahal kanon menulis `amount/value` dan `code` sebagai string;
- `set_payment_terms` menulis {"text": …}, padahal R4 dan kanon memakai string;
- `set_total_net` mewajibkan currency tanpa default; kanon memakai 'IDR';
- tidak ada cancelledReason, totalGross, totalVAT, dan customer.

Quirk kanon ditiru dan ditandai:
- `set_customer` menulis elemen `subject` — nama method tidak cocok dengan elemennya;
- `add_line_item` menulis `service` dan `quantity` di dalam lineItem, keduanya bukan
  elemen Invoice.lineItem R4 (R4 memakai chargeItem[x] dan priceComponent).
"""
from typing import Any, Dict, Optional

from satusehat_integration.builder.base_builder import BaseBuilder


def _kode(system: str, code: str, display: str = "") -> Dict[str, Any]:
    return {"coding": [{"system": system, "code": code, "display": display}]}


class InvoiceBuilder(BaseBuilder):
    """Builder for Invoice resource."""

    def __init__(self):
        super().__init__("Invoice")

    def set_id(self, id: str) -> "InvoiceBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, system: str, value: str) -> "InvoiceBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_status(self, status: str) -> "InvoiceBuilder":
        self.data["status"] = status
        return self

    def set_cancelled_reason(self, reason: str) -> "InvoiceBuilder":
        self.data["cancelledReason"] = reason
        return self

    def set_type(self, system: str, code: str, display: str = "") -> "InvoiceBuilder":
        self.data["type"] = _kode(system, code, display)
        return self

    def set_date(self, date_time: str) -> "InvoiceBuilder":
        self.data["date"] = date_time
        return self

    def set_participant(
        self,
        role_system: str,
        role_code: str,
        reference: str,
        display: str = "",
    ) -> "InvoiceBuilder":
        participant: Dict[str, Any] = {
            "role": {"coding": [{"system": role_system, "code": role_code}]},
            "actor": {"reference": reference},
        }
        if display:
            participant["actor"]["display"] = display
        return self._push("participant", participant)

    def set_issuer(self, reference: str) -> "InvoiceBuilder":
        self.data["issuer"] = {"reference": reference}
        return self

    def set_customer(self, reference: str) -> "InvoiceBuilder":
        """Quirk kanon: ditulis ke elemen `subject`, bukan `customer`."""
        self.data["subject"] = {"reference": reference}
        return self

    def set_account(self, reference: str) -> "InvoiceBuilder":
        self.data["account"] = {"reference": reference}
        return self

    def add_line_item(
        self,
        sequence: int,
        service_system: str,
        service_code: str,
        service_display: str,
        quantity: Optional[float] = None,
        unit_price: Optional[float] = None,
        price_factor: Optional[float] = None,
    ) -> "InvoiceBuilder":
        line_item: Dict[str, Any] = {
            "sequence": sequence,
            "service": _kode(service_system, service_code, service_display),
        }
        if quantity is not None:
            line_item["quantity"] = {"value": quantity}
        if unit_price is not None:
            line_item.setdefault("priceComponent", []).append({"type": "base", "amount": {"value": unit_price}})
        if price_factor is not None:
            line_item.setdefault("priceComponent", []).append({"type": "factor", "factor": price_factor})
        return self._push("lineItem", line_item)

    def add_line_item_price_component(
        self, item_idx: int, type: str, amount: float, code: Optional[str] = None
    ) -> "InvoiceBuilder":
        component: Dict[str, Any] = {"type": type, "amount": {"value": amount}}
        if code:
            component["code"] = code
        return self._push(f"lineItem/{item_idx}/priceComponent", component)

    def set_total_net(self, value: float, code: str = "IDR") -> "InvoiceBuilder":
        self._set("totalNet/value", value)
        return self._set("totalNet/currency", code)

    def set_total_gross(self, value: float, code: str = "IDR") -> "InvoiceBuilder":
        self._set("totalGross/value", value)
        return self._set("totalGross/currency", code)

    def set_total_vat(self, value: float, code: str = "IDR") -> "InvoiceBuilder":
        self._set("totalVAT/value", value)
        return self._set("totalVAT/currency", code)

    def set_payment_terms(self, text: str) -> "InvoiceBuilder":
        self.data["paymentTerms"] = text
        return self

    def add_note(self, text: str) -> "InvoiceBuilder":
        return self._push("note", {"text": text})

    # --- alias nama lama ------------------------------------------------------

    def set_code(self, system: str, code: str, display: Optional[str] = None) -> "InvoiceBuilder":
        """Alias lama: dulu menulis `code`; kini menulis `type` seperti kanon."""
        return self.set_type(system, code, display or "")

    def set_subject(self, reference: str, display: Optional[str] = None) -> "InvoiceBuilder":
        self.set_customer(reference)
        if display:
            self.data["subject"]["display"] = display
        return self

    def set_participant_party(self, reference: str, display: Optional[str] = None) -> "InvoiceBuilder":
        participant: Dict[str, Any] = {"actor": {"reference": reference}}
        if display:
            participant["actor"]["display"] = display
        return self._push("participant", participant)

    def set_total_price_component(
        self, type: str, code: str, code_system: str, value: float, display: Optional[str] = None
    ) -> "InvoiceBuilder":
        component: Dict[str, Any] = {
            "type": type,
            "code": {"coding": [{"system": code_system, "code": code}]},
            "value": value,
        }
        if display:
            component["code"]["coding"][0]["display"] = display
        self.data["totalPriceComponent"] = [component]
        return self
