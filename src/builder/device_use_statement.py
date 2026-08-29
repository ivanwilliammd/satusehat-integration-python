from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class DeviceUseStatementBuilder(BaseBuilder):
    _resourceType = "DeviceUseStatement"

    def __init__(self) -> None:
        super().__init__("DeviceUseStatementBuilder")

    def status(self, value: str) -> "DeviceUseStatementBuilder":
        return self._set("status", value)

    def subject(self, reference: str, display: Optional[str] = None) -> "DeviceUseStatementBuilder":
        sub: dict = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("subject", sub)

    def encounter(self, reference: str) -> "DeviceUseStatementBuilder":
        return self._set("encounter", {"reference": reference})

    def occurrence_date_time(self, value: str) -> "DeviceUseStatementBuilder":
        return self._set("occurrenceDateTime", value)

    def occurrence_period(self, start: Optional[str] = None, end: Optional[str] = None) -> "DeviceUseStatementBuilder":
        p: dict = {}
        if start:
            p["start"] = start
        if end:
            p["end"] = end
        return self._set("occurrencePeriod", p) if p else self

    def recorded_on(self, value: str) -> "DeviceUseStatementBuilder":
        return self._set("recordedOn", value)

    def source(self, reference: str, display: Optional[str] = None) -> "DeviceUseStatementBuilder":
        src: dict = {"reference": reference}
        if display:
            src["display"] = display
        return self._set("source", src)

    def device(self, codeable_concept: dict) -> "DeviceUseStatementBuilder":
        return self._set("device", codeable_concept)

    def device_reference(self, reference: str) -> "DeviceUseStatementBuilder":
        return self._set("device", {"reference": reference})

    def reason_code(self, codeable_concept: dict) -> "DeviceUseStatementBuilder":
        return self._append("reasonCode", codeable_concept)

    def reason_reference(self, reference: str) -> "DeviceUseStatementBuilder":
        return self._append("reasonReference", {"reference": reference})

    def body_site(self, codeable_concept: dict) -> "DeviceUseStatementBuilder":
        return self._set("bodySite", codeable_concept)

    def note(self, text: str) -> "DeviceUseStatementBuilder":
        return self._append("note", {"text": text})
