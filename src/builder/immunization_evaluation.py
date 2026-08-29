from typing import Optional
from src.builder.base_builder import BaseBuilder


class ImmunizationEvaluationBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ImmunizationEvaluation")

    def set_id(id: str) -> "ImmunizationEvaluationBuilder":
        self._set("id", id)
        return self

    def add_identifier(system: str, value: str) -> "ImmunizationEvaluationBuilder":
        self._append("identifier", {"system": system, "value": value})
        return self

    def set_status(status: str) -> "ImmunizationEvaluationBuilder":
        self._set("status", status)
        return self

    def set_code(code: dict) -> "ImmunizationEvaluationBuilder":
        self._set("code", code)
        return self

    def set_subject(reference: str, display: str = None) -> "ImmunizationEvaluationBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(description: str) -> "ImmunizationEvaluationBuilder":
        self._set("description", description)
        return self
