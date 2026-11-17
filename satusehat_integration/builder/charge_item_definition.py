"""ChargeItemDefinition resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderChargeItemDefinition.php. Versi sebelumnya hanya punya sembilan
method tanpa awalan `set_`; identifier, instance, property, dan applies belum ada.
Nama lama dipertahankan sebagai alias.

Quirk PHP ditiru dan ditandai: `add_instance` menaruh `display` dan `timingDateTime`
di tingkat instance, padahal R4 menempatkan display di dalam Reference.
"""
from typing import Any, Dict, Optional

from satusehat_integration.builder.base_builder import BaseBuilder


class ChargeItemDefinitionBuilder(BaseBuilder):
    """Builder for ChargeItemDefinition resource."""

    def __init__(self) -> None:
        super().__init__("ChargeItemDefinition")

    def _push(self, key: str, value: Any) -> "ChargeItemDefinitionBuilder":  # type: ignore[override]
        self.data.setdefault(key, []).append(value)
        return self

    def set_id(self, id: str) -> "ChargeItemDefinitionBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, system: str, value: str) -> "ChargeItemDefinitionBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_url(self, url: str) -> "ChargeItemDefinitionBuilder":
        self.data["url"] = url
        return self

    def set_version(self, version: str) -> "ChargeItemDefinitionBuilder":
        self.data["version"] = version
        return self

    def set_name(self, name: str) -> "ChargeItemDefinitionBuilder":
        self.data["name"] = name
        return self

    def set_title(self, title: str) -> "ChargeItemDefinitionBuilder":
        self.data["title"] = title
        return self

    def set_status(self, status: str) -> "ChargeItemDefinitionBuilder":
        self.data["status"] = status
        return self

    def set_date(self, date: str) -> "ChargeItemDefinitionBuilder":
        self.data["date"] = date
        return self

    def set_publisher(self, publisher: str) -> "ChargeItemDefinitionBuilder":
        self.data["publisher"] = publisher
        return self

    def set_description(self, description: str) -> "ChargeItemDefinitionBuilder":
        self.data["description"] = description
        return self

    def set_code(self, system: str, code: str, display: str = "") -> "ChargeItemDefinitionBuilder":
        self.data["code"] = {"coding": [{"system": system, "code": code, "display": display}]}
        return self

    def add_instance(
        self,
        reference: Optional[str] = None,
        display: Optional[str] = None,
        timing_date_time: Optional[str] = None,
    ) -> "ChargeItemDefinitionBuilder":
        """Quirk PHP: display dan timingDateTime ditulis di tingkat instance."""
        instance: Dict[str, Any] = {}
        if reference:
            instance["reference"] = {"reference": reference}
        if display:
            instance["display"] = display
        if timing_date_time:
            instance["timingDateTime"] = timing_date_time
        return self._push("instance", instance)

    def add_property(self, code_system: str, code_value: str, value_string: str) -> "ChargeItemDefinitionBuilder":
        return self._push(
            "property",
            {
                "code": {"coding": [{"system": code_system, "code": code_value}]},
                "valueString": value_string,
            },
        )

    def add_applies(self, applies_type: str, value: str) -> "ChargeItemDefinitionBuilder":
        """PHP menulis `applies` + ucfirst(type): appliesDateTime, appliesAge, dst."""
        self.data[f"applies{applies_type[0].upper()}{applies_type[1:]}"] = value
        return self

    # --- alias nama lama ------------------------------------------------------

    def url(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self.set_url(value)

    def version(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self.set_version(value)

    def name(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self.set_name(value)

    def title(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self.set_title(value)

    def status(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self.set_status(value)

    def date(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self.set_date(value)

    def publisher(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self.set_publisher(value)

    def description(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self.set_description(value)

    def code(self, konsep: Dict[str, Any]) -> "ChargeItemDefinitionBuilder":
        return self._set("code", konsep)
