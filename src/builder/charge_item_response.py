"""ChargeItemResponse builder.

PERHATIAN: `ChargeItemResponse` bukan resource FHIR R4. R4 punya `ChargeItem` dan
`ChargeItemDefinition`; tidak ada `chargeitemresponse` di spesifikasi, dan tautan
yang ditulis di docblock PHP (`hl7.org/fhir/R4/chargeitemresponse.html`) tidak ada.
Ini resource rumahan — port ini meniru PHP apa adanya, tetapi payload-nya tidak akan
diterima server FHIR mana pun kecuali server itu memang mengenalnya.

Versi Python sebelumnya tujuh method tanpa awalan `set_`; identifier, partOf,
outcomeInfo, error, costCenterChargeItemResponse, dan responseDate belum ada.
"""
from typing import Any, Dict

from src.builder.base_builder import BaseBuilder


class ChargeItemResponseBuilder(BaseBuilder):
    """Builder untuk resource rumahan ChargeItemResponse (bukan R4)."""

    def __init__(self) -> None:
        super().__init__("ChargeItemResponse")

    def _push(self, key: str, value: Any) -> "ChargeItemResponseBuilder":  # type: ignore[override]
        self.data.setdefault(key, []).append(value)
        return self

    def set_id(self, id: str) -> "ChargeItemResponseBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, system: str, value: str) -> "ChargeItemResponseBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_status(self, status: str) -> "ChargeItemResponseBuilder":
        self.data["status"] = status
        return self

    def set_charge_item(self, reference: str) -> "ChargeItemResponseBuilder":
        self.data["chargeItem"] = {"reference": reference}
        return self

    def set_part_of(self, reference: str) -> "ChargeItemResponseBuilder":
        return self._push("partOf", {"reference": reference})

    def set_request(self, reference: str) -> "ChargeItemResponseBuilder":
        self.data["request"] = {"reference": reference}
        return self

    def set_outcome(self, system: str, code: str, display: str = "") -> "ChargeItemResponseBuilder":
        self.data["outcome"] = {"coding": [{"system": system, "code": code, "display": display}]}
        return self

    def set_description(self, description: str) -> "ChargeItemResponseBuilder":
        self.data["description"] = description
        return self

    def set_created(self, created: str) -> "ChargeItemResponseBuilder":
        self.data["created"] = created
        return self

    def set_requestor(self, reference: str) -> "ChargeItemResponseBuilder":
        self.data["requestor"] = {"reference": reference}
        return self

    def add_outcome_info(self, system: str, code: str, display: str = "") -> "ChargeItemResponseBuilder":
        return self._push("outcomeInfo", {"code": {"coding": [{"system": system, "code": code, "display": display}]}})

    def add_error(self, system: str, code: str, display: str = "") -> "ChargeItemResponseBuilder":
        return self._push("error", {"code": {"coding": [{"system": system, "code": code, "display": display}]}})

    def add_cost_center_charge_item_response(
        self, reference: str, display: str = ""
    ) -> "ChargeItemResponseBuilder":
        response: Dict[str, Any] = {"costCenter": {"reference": reference}}
        if display:
            response["costCenter"]["display"] = display
        return self._push("costCenterChargeItemResponse", response)

    def set_response_date(self, date: str) -> "ChargeItemResponseBuilder":
        self.data["responseDate"] = date
        return self

    # --- alias nama lama ------------------------------------------------------

    def status(self, value: str) -> "ChargeItemResponseBuilder":
        return self.set_status(value)

    def charge_item(self, reference: str) -> "ChargeItemResponseBuilder":
        return self.set_charge_item(reference)

    def request(self, reference: str) -> "ChargeItemResponseBuilder":
        return self.set_request(reference)

    def outcome(self, konsep: Dict[str, Any]) -> "ChargeItemResponseBuilder":
        return self._set("outcome", konsep)

    def description(self, value: str) -> "ChargeItemResponseBuilder":
        return self.set_description(value)

    def created(self, value: str) -> "ChargeItemResponseBuilder":
        return self.set_created(value)

    def requestor(self, reference: str) -> "ChargeItemResponseBuilder":
        return self.set_requestor(reference)
