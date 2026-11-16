"""CommunicationParser — typed accessors over the official SATUSEHAT Communication payload.

Shape source: satusehat-conformance/examples/satusehat/Communication.json, copied unchanged to
src/parser/testdata/Communication.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class CommunicationParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_based_on(self) -> Any:
        return self.payload.get("basedOn")

    getBasedOn = get_based_on

    def get_payload(self) -> Any:
        return self.payload.get("payload")

    getPayload = get_payload

    def get_about(self) -> Any:
        return self.payload.get("about")

    getAbout = get_about

    def get_in_response_to(self) -> Any:
        return self.payload.get("inResponseTo")

    getInResponseTo = get_in_response_to

    def get_sender(self) -> Any:
        return self.payload.get("sender")

    getSender = get_sender

    def get_recipient(self) -> Any:
        return self.payload.get("recipient")

    getRecipient = get_recipient

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_code(self) -> Any:
        return self._data.get("code")

    getCode = get_code

    def get_subject(self) -> Any:
        return self._data.get("subject")

    getSubject = get_subject

    def get_description(self) -> Any:
        return self._data.get("description")

    getDescription = get_description

    def get_encounter(self) -> Any:
        return self._data.get("encounter")

    getEncounter = get_encounter

    def get_identifier(self) -> Any:
        return self._data.get("identifier")

    getIdentifier = get_identifier
