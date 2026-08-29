"""Invoice resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class InvoiceBuilder(BaseBuilder):
    """Builder for Invoice resource."""

    def __init__(self):
        super().__init__("InvoiceBuilder")
        self.data = {"resourceType": "Invoice"}

    def set_id(self, id: str) -> "InvoiceBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "InvoiceBuilder":
        self.data["status"] = status
        return self

    def set_code(self, code: str, system: str, display: Optional[str] = None) -> "InvoiceBuilder":
        self.data["code"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["code"]["coding"][0]["display"] = display
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "InvoiceBuilder":
        self.data["subject"] = {"reference": reference}
        if display:
            self.data["subject"]["display"] = display
        return self

    def set_date(self, date: str) -> "InvoiceBuilder":
        self.data["date"] = date
        return self

    def set_participant(
        self,
        role_code: str,
        role_system: str,
        actor_reference: str,
        actor_display: Optional[str] = None
    ) -> "InvoiceBuilder":
        self.data.setdefault("participant", [])
        part: dict = {
            "role": {"coding": [{"code": role_code, "system": role_system}]},
            "actor": {"reference": actor_reference}
        }
        if actor_display:
            part["actor"]["display"] = actor_display
        self.data["participant"].append(part)
        return self

    def set_participant_party(self, actor_reference: str, actor_display: Optional[str] = None) -> "InvoiceBuilder":
        self.data.setdefault("participant", [])
        part: dict = {"actor": {"reference": actor_reference}}
        if actor_display:
            part["actor"]["display"] = actor_display
        self.data["participant"].append(part)
        return self

    def set_issuer(self, reference: str, display: Optional[str] = None) -> "InvoiceBuilder":
        self.data["issuer"] = {"reference": reference}
        if display:
            self.data["issuer"]["display"] = display
        return self

    def set_account(self, reference: str) -> "InvoiceBuilder":
        self.data["account"] = {"reference": reference}
        return self

    def add_line_item(
        self,
        sequence: int,
        service_code: str,
        service_system: str,
        service_display: Optional[str] = None
    ) -> "InvoiceBuilder":
        self.data.setdefault("lineItem", [])
        line: dict = {
            "sequence": str(sequence),
            "service": {"coding": [{"code": service_code, "system": service_system}]}
        }
        if service_display:
            line["service"]["coding"][0]["display"] = service_display
        self.data["lineItem"].append(line)
        return self

    def add_line_item_price_component(
        self,
        line_index: int,
        type_code: str,
        code: str,
        code_system: str,
        value: float
    ) -> "InvoiceBuilder":
        if "lineItem" in self.data and len(self.data["lineItem"]) > line_index:
            self.data["lineItem"][line_index].setdefault("priceComponent", [])
            comp: dict = {"type": type_code, "code": {"coding": [{"code": code, "system": code_system}]}, "value": value}
            self.data["lineItem"][line_index]["priceComponent"].append(comp)
        return self

    def set_total_price_component(
        self,
        type_code: str,
        code: str,
        code_system: str,
        value: float,
        display: Optional[str] = None
    ) -> "InvoiceBuilder":
        comp: dict = {
            "type": type_code,
            "code": {"coding": [{"code": code, "system": code_system}]},
            "value": value
        }
        if display:
            comp["code"]["coding"][0]["display"] = display
        self.data["totalPriceComponent"] = [comp]
        return self

    def set_total_net(self, value: float, currency: str) -> "InvoiceBuilder":
        self.data["totalNet"] = {"value": value, "currency": currency}
        return self

    def set_payment_terms(self, text: str) -> "InvoiceBuilder":
        self.data["paymentTerms"] = {"text": text}
        return self

    def add_note(self, text: str) -> "InvoiceBuilder":
        self.data.setdefault("note", [])
        self.data["note"].append({"text": text})
        return self
