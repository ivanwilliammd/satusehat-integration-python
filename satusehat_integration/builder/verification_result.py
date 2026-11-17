from typing import Optional
from satusehat_integration.builder.base_builder import BaseBuilder


class VerificationResultBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("VerificationResult")

    def set_id(self, id: str) -> "VerificationResultBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "VerificationResultBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "VerificationResultBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "VerificationResultBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "VerificationResultBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "VerificationResultBuilder":
        self._set("description", description)
        return self

    def set_encounter(self, reference: str) -> "VerificationResultBuilder":
        self._set("encounter", {"reference": reference})
        return self
