"""ChargeItem resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderChargeItem.php. Versi sebelumnya menulis elemen yang berbeda
dari kanon: `encounter` (R4 dan PHP memakai `context`), `quantity` sebagai objek
Quantity (PHP menulis angka), dan `bodySite` sebagai satu objek, bukan daftar.

Karena kanon adalah PHP, port ini mengikuti PHP dan menandai quirk-nya. Nama lama
dipertahankan sebagai alias, tetapi tujuannya dibetulkan.
"""
from typing import Any, Dict, Optional

from src.builder.base_builder import BaseBuilder


def _kode(system: str, code: str, display: str = "") -> Dict[str, Any]:
    return {"coding": [{"system": system, "code": code, "display": display}]}


class ChargeItemBuilder(BaseBuilder):
    """Builder for ChargeItem resource."""

    def __init__(self):
        super().__init__("ChargeItem")

    def _push(self, key: str, value: Any) -> "ChargeItemBuilder":  # type: ignore[override]
        self.data.setdefault(key, []).append(value)
        return self

    def set_id(self, id: str) -> "ChargeItemBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, system: str, value: str) -> "ChargeItemBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_status(self, status: str) -> "ChargeItemBuilder":
        self.data["status"] = status
        return self

    def set_part_of(self, reference: str) -> "ChargeItemBuilder":
        return self._push("partOf", {"reference": reference})

    def set_code(self, system: str, code: str, display: str = "") -> "ChargeItemBuilder":
        self.data["code"] = _kode(system, code, display)
        return self

    def set_subject(self, reference: str) -> "ChargeItemBuilder":
        self.data["subject"] = {"reference": reference}
        return self

    def set_focus(self, reference: str) -> "ChargeItemBuilder":
        self.data["focus"] = {"reference": reference}
        return self

    def set_encounter(self, reference: str) -> "ChargeItemBuilder":
        """FHIR R4 menamai elemen ini `context`, bukan `encounter`. PHP begitu juga."""
        self.data["context"] = {"reference": reference}
        return self

    def set_performed_date(self, date_time: str) -> "ChargeItemBuilder":
        self.data["performedDateTime"] = date_time
        return self

    def set_performer_actor(
        self,
        reference: str,
        function_system: Optional[str] = None,
        function_code: Optional[str] = None,
    ) -> "ChargeItemBuilder":
        performer: Dict[str, Any] = {"actor": {"reference": reference}}
        if function_system and function_code:
            performer["function"] = {"coding": [{"system": function_system, "code": function_code}]}
        return self._push("performer", performer)

    def set_performer_cost_center(self, reference: str) -> "ChargeItemBuilder":
        return self._push("performer", {"actor": {"reference": reference}})

    def set_organization(self, reference: str) -> "ChargeItemBuilder":
        self.data["performingOrganization"] = {"reference": reference}
        return self

    def set_requesting_organization(self, reference: str) -> "ChargeItemBuilder":
        self.data["requestingOrganization"] = {"reference": reference}
        return self

    def set_quantity(self, quantity: int) -> "ChargeItemBuilder":
        """Quirk PHP: `quantity` di FHIR bertipe Quantity, di sini ditulis angka."""
        self.data["quantity"] = quantity
        return self

    def set_bodysite(self, system: str, code: str, display: str = "") -> "ChargeItemBuilder":
        return self._push("bodysite", _kode(system, code, display))

    def set_product_code(self, system: str, code: str, display: str = "") -> "ChargeItemBuilder":
        self.data["productCodeableConcept"] = _kode(system, code, display)
        return self

    def set_price_override(self, value: float, code: str = "IDR") -> "ChargeItemBuilder":
        self.data["priceOverride"] = {"value": value, "currency": code}
        return self

    def set_override_reason(self, override_reason: str) -> "ChargeItemBuilder":
        self.data["overrideReason"] = override_reason
        return self

    def set_enterer(self, reference: str) -> "ChargeItemBuilder":
        self.data["enterer"] = {"reference": reference}
        return self

    def set_entered_date(self, date_time: str) -> "ChargeItemBuilder":
        self.data["enteredDate"] = date_time
        return self

    def set_reason(self, system: str, code: str, display: str = "") -> "ChargeItemBuilder":
        return self._push("reason", _kode(system, code, display))

    def set_service(self, reference: str) -> "ChargeItemBuilder":
        return self._push("service", {"reference": reference})

    def set_account(self, reference: str) -> "ChargeItemBuilder":
        return self._push("account", {"reference": reference})

    # --- alias nama lama ------------------------------------------------------

    def set_occurence_datetime(self, value: str) -> "ChargeItemBuilder":
        return self.set_performed_date(value)

    def set_performing_organization(self, reference: str, display: Optional[str] = None) -> "ChargeItemBuilder":
        self.set_organization(reference)
        if display:
            self.data["performingOrganization"]["display"] = display
        return self

    def add_factor_override(self, factor: float) -> "ChargeItemBuilder":
        self.data["factorOverride"] = factor
        return self

    def add_reason(self, system: str, code: str, display: str = "") -> "ChargeItemBuilder":
        return self.set_reason(system, code, display)

    def add_service(self, reference: str) -> "ChargeItemBuilder":
        return self.set_service(reference)

    def set_performer(
        self,
        function_code: str,
        function_system: str,
        actor_reference: str,
        actor_display: Optional[str] = None,
    ) -> "ChargeItemBuilder":
        """Alias lama: argumennya (function_code, function_system, actor) — bukan bentuk PHP."""
        performer: Dict[str, Any] = {
            "function": {"coding": [{"system": function_system, "code": function_code}]},
            "actor": {"reference": actor_reference},
        }
        if actor_display:
            performer["actor"]["display"] = actor_display
        return self._push("performer", performer)
