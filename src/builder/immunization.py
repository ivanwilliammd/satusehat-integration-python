from typing import List, Optional
from typing import Any

from src.builder.base_builder import BaseBuilder


def _arr(value: Any) -> Any:
    return value.to_array() if hasattr(value, "to_array") else value


class ImmunizationBuilder(BaseBuilder):
    _resourceType = "Immunization"

    def __init__(self) -> None:
        super().__init__("Immunization")

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

    # --- Nama kanon (cermin PayloadBuilderImmunization), di samping API fluent lama ---

    def set_id(self, id: str) -> "ImmunizationBuilder":
        return self._set("id", id)

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "ImmunizationBuilder":
        if value is not None:
            return self._push("identifier", {"system": identifier, "value": value})
        return self._push("identifier", _arr(identifier))

    def set_meta_profile(self, profile: str) -> "ImmunizationBuilder":
        self.data.setdefault("meta", {})["profile"] = [profile]
        return self

    def set_vaccine_code(self, vaccine_code: Any) -> "ImmunizationBuilder":
        return self._set("vaccineCode", _arr(vaccine_code))

    def set_patient(self, reference: Any, display: Optional[str] = None) -> "ImmunizationBuilder":
        if isinstance(reference, str):
            ref: dict = {"reference": reference}
            if display:
                ref["display"] = display
            return self._set("patient", ref)
        return self._set("patient", _arr(reference))

    def set_occurrence_date_time(self, date_time: str) -> "ImmunizationBuilder":
        return self._set("occurrenceDateTime", date_time)

    def add_performer(self, actor: Any, function: Any = None) -> "ImmunizationBuilder":
        if isinstance(actor, str):
            entry: dict = {"actor": {"reference": actor}}
        else:
            entry = {"actor": _arr(actor)}
        if function is not None:
            entry["function"] = _arr(function)
        return self._push("performer", entry)

    def set_dose_quantity(self, value: float, unit: str, code: Optional[str] = None,
                          system: str = "http://unitsofmeasure.org") -> "ImmunizationBuilder":
        quantity: dict = {"value": value, "unit": unit}
        if code is not None:
            quantity["system"] = system
            quantity["code"] = code
        return self._set("doseQuantity", quantity)

    def set_location(self, reference: Any, display: Optional[str] = None) -> "ImmunizationBuilder":
        if isinstance(reference, str):
            loc: dict = {"reference": reference}
            if display:
                loc["display"] = display
            return self._set("location", loc)
        return self._set("location", _arr(reference))

    def set_lot_number(self, lot_number: str) -> "ImmunizationBuilder":
        return self._set("lotNumber", lot_number)

    def set_recorded(self, recorded: str) -> "ImmunizationBuilder":
        return self._set("recorded", recorded)

    def set_primary_source(self, primary_source: bool) -> "ImmunizationBuilder":
        return self._set("primarySource", primary_source)

    def add_protocol_applied(self, dose_number_positive_int: int, series: Any = None,
                             series_doses_positive_int: Optional[int] = None) -> "ImmunizationBuilder":
        # FHIR R4: series adalah CodeableConcept, seriesDoses[x] elemen terpisah.
        row: dict = {"doseNumberPositiveInt": dose_number_positive_int}
        if series is not None:
            row["series"] = _arr(series)
        if series_doses_positive_int is not None:
            row["seriesDosesPositiveInt"] = series_doses_positive_int
        return self._push("protocolApplied", row)

    def set_route(self, route: Any) -> "ImmunizationBuilder":
        return self._set("route", _arr(route))

    def add_reason_code(self, reason_code: Any) -> "ImmunizationBuilder":
        return self._push("reasonCode", _arr(reason_code))

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "ImmunizationBuilder":
        extension: dict = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        return self._push("extension", extension)
