"""Substance resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderSubstance.php. Versi sebelumnya lima method tanpa awalan `set_`;
`id` dan Narrative (`text`) belum ada, dan `status` tidak divalidasi.

Kanon hanya punya empat setter; sisanya di sini (identifier, category, description)
adalah tambahan yang sah R4 dan tidak ditulis kanon — dibuktikan lewat uji.
"""
from typing import Any, Dict, Optional

from satusehat_integration.builder.base_builder import BaseBuilder


class SubstanceBuilder(BaseBuilder):
    """Builder for Substance resource."""

    VALID_STATUSES = ["active", "inactive", "entered-in-error"]

    def __init__(self) -> None:
        super().__init__("Substance")

    def set_id(self, id: str) -> "SubstanceBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "SubstanceBuilder":
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        self.data["status"] = status
        return self

    def set_code(self, system: Any, code: Optional[str] = None, display: str = "") -> "SubstanceBuilder":
        if isinstance(system, dict):
            self.data["code"] = system
            return self
        self.data["code"] = {"coding": [{"system": system, "code": code or "", "display": display}]}
        return self

    def set_text(self, status: str, div: str) -> "SubstanceBuilder":
        self.data["text"] = {"status": status, "div": div}
        return self

    # --- tambahan yang sah R4, tidak ditulis kanon ----------------------------

    def add_identifier(self, system: str, value: str) -> "SubstanceBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def add_category(self, konsep: Dict[str, Any]) -> "SubstanceBuilder":
        return self._push("category", konsep)

    def set_description(self, description: str) -> "SubstanceBuilder":
        self.data["description"] = description
        return self

    # --- alias nama lama ------------------------------------------------------

    def identifier(self, system: str, value: str) -> "SubstanceBuilder":
        return self.add_identifier(system, value)

    def status(self, value: str) -> "SubstanceBuilder":
        return self.set_status(value)

    def category(self, konsep: Dict[str, Any]) -> "SubstanceBuilder":
        return self.add_category(konsep)

    def code(self, konsep: Dict[str, Any]) -> "SubstanceBuilder":
        return self.set_code(konsep)

    def description(self, value: str) -> "SubstanceBuilder":
        return self.set_description(value)
