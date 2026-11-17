from typing import Optional
from satusehat_integration.builder.base_builder import BaseBuilder


class MeasureReportBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("MeasureReport")

    def set_id(self, id: str) -> "MeasureReportBuilder":
        self._set("id", id)
        return self

    def add_identifier(self, system: str, value: str) -> "MeasureReportBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "MeasureReportBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "MeasureReportBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "MeasureReportBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "MeasureReportBuilder":
        self._set("description", description)
        return self

    def set_encounter(self, reference: str) -> "MeasureReportBuilder":
        self._set("encounter", {"reference": reference})
        return self
