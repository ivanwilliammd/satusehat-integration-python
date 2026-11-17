"""DeviceUseStatementParser — typed accessors over the official SATUSEHAT DeviceUseStatement payload.

Shape source: satusehat-conformance/examples/satusehat/DeviceUseStatement.json, copied unchanged to
satusehat_integration/parser/testdata/DeviceUseStatement.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class DeviceUseStatementParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_identifier(self) -> Any:
        return self.payload.get("identifier")

    getIdentifier = get_identifier

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_device(self) -> Any:
        return self.payload.get("device")

    getDevice = get_device

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_timing_period(self) -> Any:
        return self.payload.get("timingPeriod")

    getTimingPeriod = get_timing_period

    def get_recorded_on(self) -> Any:
        return self.payload.get("recordedOn")

    getRecordedOn = get_recorded_on

    def get_source(self) -> Any:
        return self.payload.get("source")

    getSource = get_source

    def get_reason_code(self) -> Any:
        return self.payload.get("reasonCode")

    getReasonCode = get_reason_code

    def get_note(self) -> Any:
        return self.payload.get("note")

    getNote = get_note

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_code(self) -> Any:
        return self._data.get("code")

    getCode = get_code

    def get_description(self) -> Any:
        return self._data.get("description")

    getDescription = get_description

    def get_encounter(self) -> Any:
        return self._data.get("encounter")

    getEncounter = get_encounter
