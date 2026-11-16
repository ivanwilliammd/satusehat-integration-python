"""ChargeItemResponseParser — typed accessors over the official SATUSEHAT ChargeItemResponse payload.

Shape source: satusehat-conformance/examples/satusehat/ChargeItemResponse.json, copied unchanged to
src/parser/testdata/ChargeItemResponse.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class ChargeItemResponseParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_id(self) -> Any:
        return self.payload.get("id")

    getId = get_id

    def get_identifier(self) -> Any:
        return self.payload.get("identifier")

    getIdentifier = get_identifier

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_charge_item(self) -> Any:
        return self.payload.get("chargeItem")

    getChargeItem = get_charge_item

    def get_coverage(self) -> Any:
        return self.payload.get("coverage")

    getCoverage = get_coverage

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_encounter(self) -> Any:
        return self.payload.get("encounter")

    getEncounter = get_encounter

    def get_payor(self) -> Any:
        return self.payload.get("payor")

    getPayor = get_payor

    def get_quantity(self) -> Any:
        return self.payload.get("quantity")

    getQuantity = get_quantity

    def get_unit_price_override(self) -> Any:
        return self.payload.get("unitPriceOverride")

    getUnitPriceOverride = get_unit_price_override

    def get_factor_override(self) -> Any:
        return self.payload.get("factorOverride")

    getFactorOverride = get_factor_override

    def get_override_reason(self) -> Any:
        return self.payload.get("overrideReason")

    getOverrideReason = get_override_reason

    def get_total(self) -> Any:
        return self.payload.get("total")

    getTotal = get_total

    def get_excess(self) -> Any:
        return self.payload.get("excess")

    getExcess = get_excess

    def get_outcome(self) -> Any:
        return self._data.get("outcome")

    getOutcome = get_outcome
