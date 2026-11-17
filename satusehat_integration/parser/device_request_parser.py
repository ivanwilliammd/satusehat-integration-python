"""DeviceRequestParser — typed accessors over the official SATUSEHAT DeviceRequest payload.

Shape source: satusehat-conformance/examples/satusehat/DeviceRequest.json, copied unchanged to
satusehat_integration/parser/testdata/DeviceRequest.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class DeviceRequestParser:
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

    def get_intent(self) -> Any:
        return self.payload.get("intent")

    getIntent = get_intent

    def get_priority(self) -> Any:
        return self.payload.get("priority")

    getPriority = get_priority

    def get_code_reference(self) -> Any:
        return self.payload.get("codeReference")

    getCodeReference = get_code_reference

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_authored_on(self) -> Any:
        return self.payload.get("authoredOn")

    getAuthoredOn = get_authored_on

    def get_requester(self) -> Any:
        return self.payload.get("requester")

    getRequester = get_requester

    def get_performer(self) -> Any:
        return self.payload.get("performer")

    getPerformer = get_performer

    def get_reason_code(self) -> Any:
        return self.payload.get("reasonCode")

    getReasonCode = get_reason_code

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
