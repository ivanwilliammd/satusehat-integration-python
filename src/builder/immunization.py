from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class ImmunizationBuilder(BaseBuilder):
    _resourceType = "Immunization"

    def __init__(self) -> None:
        super().__init__("ImmunizationBuilder")

    def status(self, value: str) -> "ImmunizationBuilder":
        return self._set("status", value)

    def vaccine_code(self, codeable_concept: dict) -> "ImmunizationBuilder":
        return self._set("vaccineCode", codeable_concept)

    def subject(self, reference: str, display: Optional[str] = None) -> "ImmunizationBuilder":
        sub: dict = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("subject", sub)

    def encounter(self, reference: str) -> "ImmunizationBuilder":
        return self._set("encounter", {"reference": reference})

    def occurrence_date_time(self, value: str) -> "ImmunizationBuilder":
        return self._set("occurrenceDateTime", value)

    def recorded(self, value: str) -> "ImmunizationBuilder":
        return self._set("recorded", value)

    def primary_source(self, value: bool) -> "ImmunizationBuilder":
        return self._set("primarySource", value)

    def report_origin(self, codeable_concept: dict) -> "ImmunizationBuilder":
        return self._set("reportOrigin", codeable_concept)

    def location(self, reference: str) -> "ImmunizationBuilder":
        return self._set("location", {"reference": reference})

    def manufacturer(self, display: Optional[str] = None, reference: Optional[str] = None) -> "ImmunizationBuilder":
        mfr: dict = {}
        if display:
            mfr["display"] = display
        if reference:
            mfr["reference"] = reference
        return self._set("manufacturer", mfr) if mfr else self

    def lot_number(self, value: str) -> "ImmunizationBuilder":
        return self._set("lotNumber", value)

    def expiration_date(self, value: str) -> "ImmunizationBuilder":
        return self._set("expirationDate", value)

    def site(self, codeable_concept: dict) -> "ImmunizationBuilder":
        return self._set("site", codeable_concept)

    def route(self, codeable_concept: dict) -> "ImmunizationBuilder":
        return self._set("route", codeable_concept)

    def dose_quantity(self, value: float, unit: str, code: str, system: str = "http://unitsofmeasure.org") -> "ImmunizationBuilder":
        return self._set("doseQuantity", {"value": value, "unit": unit, "code": code, "system": system})

    def performer(self, actor_reference: str, display: Optional[str] = None) -> "ImmunizationBuilder":
        actor: dict = {"reference": actor_reference}
        if display:
            actor["display"] = display
        return self._append("performer", {"actor": actor})

    def note(self, text: str) -> "ImmunizationBuilder":
        return self._append("note", {"text": text})

    def reason_code(self, codeable_concept: dict) -> "ImmunizationBuilder":
        return self._append("reasonCode", codeable_concept)

    def reason_reference(self, reference: str) -> "ImmunizationBuilder":
        return self._set("reasonReference", {"reference": reference})

    def is_subpotent(self, value: bool) -> "ImmunizationBuilder":
        return self._set("isSubpotent", value)

    def subpotent_reason(self, codeable_concept: dict) -> "ImmunizationBuilder":
        return self._append("subpotentReason", codeable_concept)
