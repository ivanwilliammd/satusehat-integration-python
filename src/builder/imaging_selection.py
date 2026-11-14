from typing import Optional
from src.builder.base_builder import BaseBuilder


class ImagingSelectionBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ImagingSelection")

    def set_id(self, id: str) -> "ImagingSelectionBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "ImagingSelectionBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "ImagingSelectionBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "ImagingSelectionBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "ImagingSelectionBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "ImagingSelectionBuilder":
        self._set("description", description)
        return self
