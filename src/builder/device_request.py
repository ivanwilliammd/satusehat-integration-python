from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class DeviceRequestBuilder(BaseBuilder):
    _resourceType = "DeviceRequest"

    def __init__(self) -> None:
        super().__init__("DeviceRequestBuilder")

    def status(self, value: str) -> "DeviceRequestBuilder":
        return self._set("status", value)

    def intent(self, value: str) -> "DeviceRequestBuilder":
        return self._set("intent", value)

    def code(self, codeable_concept: dict) -> "DeviceRequestBuilder":
        return self._set("codeCodeableConcept", codeable_concept)

    def code_reference(self, reference: str) -> "DeviceRequestBuilder":
        return self._set("codeReference", {"reference": reference})

    def subject(self, reference: str, display: Optional[str] = None) -> "DeviceRequestBuilder":
        sub: dict = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("subject", sub)

    def encounter(self, reference: str) -> "DeviceRequestBuilder":
        return self._set("encounter", {"reference": reference})

    def occurrence_date_time(self, value: str) -> "DeviceRequestBuilder":
        return self._set("occurrenceDateTime", value)

    def occurrence_period(self, start: Optional[str] = None, end: Optional[str] = None) -> "DeviceRequestBuilder":
        p: dict = {}
        if start:
            p["start"] = start
        if end:
            p["end"] = end
        return self._set("occurrencePeriod", p) if p else self

    def authored_on(self, value: str) -> "DeviceRequestBuilder":
        return self._set("authoredOn", value)

    def requester(self, reference: str, display: Optional[str] = None) -> "DeviceRequestBuilder":
        req: dict = {"reference": reference}
        if display:
            req["display"] = display
        return self._set("requester", req)

    def performer(self, reference: str, display: Optional[str] = None) -> "DeviceRequestBuilder":
        perf: dict = {"reference": reference}
        if display:
            perf["display"] = display
        return self._set("performer", perf)

    def performer_type(self, codeable_concept: dict) -> "DeviceRequestBuilder":
        return self._set("performerType", codeable_concept)

    def reason_code(self, codeable_concept: dict) -> "DeviceRequestBuilder":
        return self._append("reasonCode", codeable_concept)

    def reason_reference(self, reference: str) -> "DeviceRequestBuilder":
        return self._append("reasonReference", {"reference": reference})

    def supporting_info(self, reference: str) -> "DeviceRequestBuilder":
        return self._append("supportingInfo", {"reference": reference})

    def note(self, text: str) -> "DeviceRequestBuilder":
        return self._append("note", {"text": text})

    def relevant_history(self, reference: str) -> "DeviceRequestBuilder":
        return self._append("relevantHistory", {"reference": reference})
