"""MessageHeader resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class MessageHeaderBuilder(BaseBuilder):
    """Builder for MessageHeader resource."""

    def __init__(self):
        super().__init__("MessageHeaderBuilder")
        self.data = {"resourceType": "MessageHeader"}

    def set_id(self, id: str) -> "MessageHeaderBuilder":
        self.data["id"] = id
        return self

    def set_event_code(self, code: str, system: str, display: Optional[str] = None) -> "MessageHeaderBuilder":
        self.data["eventCoding"] = {"code": code, "system": system}
        if display:
            self.data["eventCoding"]["display"] = display
        return self

    def set_destination(
        self,
        name: str,
        endpoint: str,
        receiver_reference: Optional[str] = None,
        receiver_display: Optional[str] = None
    ) -> "MessageHeaderBuilder":
        dest: dict = {"name": name, "endpoint": endpoint}
        if receiver_reference:
            dest["receiver"] = {"reference": receiver_reference}
            if receiver_display:
                dest["receiver"]["display"] = receiver_display
        self.data["destination"] = [dest]
        return self

    def set_sender(self, reference: str, display: Optional[str] = None) -> "MessageHeaderBuilder":
        self.data["sender"] = {"reference": reference}
        if display:
            self.data["sender"]["display"] = display
        return self

    def add_recipient(self, reference: str, display: Optional[str] = None) -> "MessageHeaderBuilder":
        self.data.setdefault("recipient", [])
        recipient: dict = {"reference": reference}
        if display:
            recipient["display"] = display
        self.data["recipient"].append(recipient)
        return self

    def set_response(self, identifier: str, code: str, details: Optional[str] = None) -> "MessageHeaderBuilder":
        self.data["response"] = {"identifier": identifier, "code": code}
        if details:
            self.data["response"]["details"] = {"reference": details}
        return self

    def set_focus(self, reference: str) -> "MessageHeaderBuilder":
        self.data["focus"] = [{"reference": reference}]
        return self

    def set_source(
        self,
        name: str,
        endpoint: str,
        software: Optional[str] = None,
        version: Optional[str] = None
    ) -> "MessageHeaderBuilder":
        self.data["source"] = {"name": name, "endpoint": endpoint}
        if software:
            self.data["source"]["software"] = software
        if version:
            self.data["source"]["version"] = version
        return self
