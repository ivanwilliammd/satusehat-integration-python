"""DeviceDispenseParser — typed accessors over the official SATUSEHAT DeviceDispense payload.

Shape source: satusehat-conformance/examples/satusehat/DeviceDispense.json, copied unchanged to
src/parser/testdata/DeviceDispense.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class DeviceDispenseParser:
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

    def get_based_on(self) -> Any:
        return self.payload.get("basedOn")

    getBasedOn = get_based_on

    def get_device(self) -> Any:
        return self.payload.get("device")

    getDevice = get_device

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_receiver(self) -> Any:
        return self.payload.get("receiver")

    getReceiver = get_receiver

    def get_performer(self) -> Any:
        return self.payload.get("performer")

    getPerformer = get_performer

    def get_when_prepared(self) -> Any:
        return self.payload.get("whenPrepared")

    getWhenPrepared = get_when_prepared

    def get_when_handed_over(self) -> Any:
        return self.payload.get("whenHandedOver")

    getWhenHandedOver = get_when_handed_over

    def get_destination(self) -> Any:
        return self.payload.get("destination")

    getDestination = get_destination

    def get_note(self) -> Any:
        return self.payload.get("note")

    getNote = get_note
