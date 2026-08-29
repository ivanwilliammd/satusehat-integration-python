from typing import Optional
from src.builder.base_builder import BaseBuilder


class CommunicationRequestBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("CommunicationRequest")

    def set_id(id: str) -> "CommunicationRequestBuilder":
        self._set("id", id)
        return self

    def add_identifier(system: str, value: str) -> "CommunicationRequestBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(status: str) -> "CommunicationRequestBuilder":
        self._set("status", status)
        return self

    def set_code(code: dict) -> "CommunicationRequestBuilder":
        self._set("code", code)
        return self

    def set_subject(reference: str, display: str = None) -> "CommunicationRequestBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(description: str) -> "CommunicationRequestBuilder":
        self._set("description", description)
        return self
