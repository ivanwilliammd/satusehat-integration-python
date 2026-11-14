"""Observation FHIR R4 resource builder.

Cermin dari PayloadBuilderObservation pada SDK PHP: 33 metode, termasuk seluruh varian value[x]
dan effective[x]. Bentuk payload diuji terhadap golden yang sama dipakai port Go dan Node.
"""

from typing import Any, Dict, Optional

from src.builder.base_builder import BaseBuilder


def _arr(value: Any) -> Any:
    """Terima objek datatype (punya to_array) atau dict siap pakai."""
    return value.to_array() if hasattr(value, "to_array") else value


class ObservationBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("Observation")

    def set_id(self, id: str) -> "ObservationBuilder":
        return self._set("id", id)

    def add_identifier(self, identifier: Any) -> "ObservationBuilder":
        return self._push("identifier", _arr(identifier))

    def set_status(self, status: str) -> "ObservationBuilder":
        return self._set("status", status)

    def add_category(self, category: Any) -> "ObservationBuilder":
        # String dilewatkan resolver terminologi pada PHP; di sini dict/datatype diterima apa adanya.
        return self._push("category", _arr(category))

    def set_code(self, code: Any) -> "ObservationBuilder":
        return self._set("code", _arr(code))

    def set_subject(self, subject: Any) -> "ObservationBuilder":
        return self._set("subject", _arr(subject))

    def set_encounter(self, encounter: Any) -> "ObservationBuilder":
        return self._set("encounter", _arr(encounter))

    def set_effective_date_time(self, date_time: str) -> "ObservationBuilder":
        return self._set("effectiveDateTime", date_time)

    def set_effective_period(self, period: Any) -> "ObservationBuilder":
        return self._set("effectivePeriod", _arr(period))

    def set_effective_instant(self, instant: str) -> "ObservationBuilder":
        return self._set("effectiveInstant", instant)

    def set_effective_timing(self, timing: Any) -> "ObservationBuilder":
        return self._set("effectiveTiming", _arr(timing))

    def set_effective_period_start(self, start: str) -> "ObservationBuilder":
        return self._set("effectivePeriod", {"start": start})

    def set_effective_period_end(self, end: str) -> "ObservationBuilder":
        existing = dict(self.data.get("effectivePeriod") or {})
        existing["end"] = end
        return self._set("effectivePeriod", existing)

    def set_value_quantity(self, value: Any) -> "ObservationBuilder":
        return self._set("valueQuantity", _arr(value))

    def set_value_codeable_concept(self, value: Any) -> "ObservationBuilder":
        return self._set("valueCodeableConcept", _arr(value))

    def set_value_string(self, value: str) -> "ObservationBuilder":
        return self._set("valueString", value)

    def set_value_boolean(self, value: bool) -> "ObservationBuilder":
        return self._set("valueBoolean", value)

    def set_value_integer(self, value: int) -> "ObservationBuilder":
        return self._set("valueInteger", value)

    def set_value_range(self, value: Any) -> "ObservationBuilder":
        return self._set("valueRange", _arr(value))

    def set_value_ratio(self, value: Any) -> "ObservationBuilder":
        return self._set("valueRatio", _arr(value))

    def set_value_time(self, value: str) -> "ObservationBuilder":
        return self._set("valueTime", value)

    def set_value_date_time(self, value: str) -> "ObservationBuilder":
        return self._set("valueDateTime", value)

    def set_value_period(self, value: Any) -> "ObservationBuilder":
        return self._set("valuePeriod", _arr(value))

    def add_interpretation(self, interpretation: Any) -> "ObservationBuilder":
        return self._push("interpretation", _arr(interpretation))

    def add_note(self, note: Any) -> "ObservationBuilder":
        return self._push("note", {"text": note} if isinstance(note, str) else _arr(note))

    def add_body_site(self, body_site: Any) -> "ObservationBuilder":
        return self._push("bodySite", _arr(body_site))

    def set_method(self, method: Any) -> "ObservationBuilder":
        return self._set("method", _arr(method))

    def set_specimen(self, specimen: Any) -> "ObservationBuilder":
        return self._set("specimen", _arr(specimen))

    def set_device(self, device: Any) -> "ObservationBuilder":
        return self._set("device", _arr(device))

    def add_reference_range(
        self,
        low: Any = None,
        high: Any = None,
        range_type: Any = None,
        text: Optional[str] = None,
    ) -> "ObservationBuilder":
        row: Dict[str, Any] = {}
        if low is not None or high is not None:
            if low is not None:
                row["low"] = _arr(low)
            if high is not None:
                row["high"] = _arr(high)
        if range_type is not None:
            row["type"] = _arr(range_type)
        if text is not None:
            row["text"] = text
        return self._push("referenceRange", row)

    def add_component(self, code: Any, value: Any) -> "ObservationBuilder":
        component: Dict[str, Any] = {"code": _arr(code)}
        if isinstance(value, str):
            component["valueString"] = value
        elif isinstance(value, bool):
            component["valueBoolean"] = value
        elif isinstance(value, int):
            component["valueInteger"] = value
        elif type(value).__name__ in ("Quantity", "CodeableConcept", "Range", "Ratio", "SampledData"):
            component["value" + type(value).__name__] = _arr(value)
        elif isinstance(value, dict):
            # PHP membedakan berdasarkan kelas datatype; di sini dict dikenali dari bentuknya.
            # ponytail: hanya Quantity/CodeableConcept yang dibedakan, tambahkan Range bila perlu.
            kunci = "valueCodeableConcept" if "coding" in value else "valueQuantity"
            component[kunci] = value
        else:
            raise TypeError(f"tipe nilai component tidak dikenal: {type(value).__name__}")
        return self._push("component", component)

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "ObservationBuilder":
        extension: Dict[str, Any] = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        return self._push("extension", extension)
