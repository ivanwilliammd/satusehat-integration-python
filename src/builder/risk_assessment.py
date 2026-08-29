"""RiskAssessment resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from .base import BaseBuilder


class RiskAssessmentBuilder(BaseBuilder):
    """Builder for RiskAssessment resource."""

    def __init__(self):
        super().__init__()
        self._data = {"resourceType": "RiskAssessment"}

    def set_id(self, id: str) -> "RiskAssessmentBuilder":
        self._data["id"] = id
        return self

    def set_status(self, status: str) -> "RiskAssessmentBuilder":
        self._data["status"] = status
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "RiskAssessmentBuilder":
        self._data["subject"] = {"reference": reference}
        if display:
            self._data["subject"]["display"] = display
        return self

    def set_encounter(self, reference: str) -> "RiskAssessmentBuilder":
        self._data["encounter"] = {"reference": reference}
        return self

    def set_occurrence_datetime(self, occurrence_datetime: str) -> "RiskAssessmentBuilder":
        self._data["occurrenceDateTime"] = occurrence_datetime
        return self

    def set_condition(self, reference: str, display: Optional[str] = None) -> "RiskAssessmentBuilder":
        self._data["condition"] = {"reference": reference}
        if display:
            self._data["condition"]["display"] = display
        return self

    def add_prediction(
        self,
        outcome: str,
        outcome_system: str,
        probability_decimal: Optional[float] = None,
        probability_range_low: Optional[float] = None,
        probability_range_high: Optional[float] = None,
        risk_direction: Optional[str] = None
    ) -> "RiskAssessmentBuilder":
        self._data.setdefault("prediction", [])
        pred: dict = {
            "outcome": {"coding": [{"code": outcome, "system": outcome_system}]}
        }
        if probability_decimal is not None:
            pred["probabilityDecimal"] = probability_decimal
        elif probability_range_low is not None or probability_range_high is not None:
            range: dict = {}
            if probability_range_low is not None:
                range["low"] = probability_range_low
            if probability_range_high is not None:
                range["high"] = probability_range_high
            pred["probabilityRange"] = range
        if risk_direction:
            pred["riskDirection"] = risk_direction
        self._data["prediction"].append(pred)
        return self

    def set_mitigation(self, mitigation: str) -> "RiskAssessmentBuilder":
        self._data["mitigation"] = mitigation
        return self

    def add_note(self, text: str) -> "RiskAssessmentBuilder":
        self._data.setdefault("note", [])
        self._data["note"].append({"text": text})
        return self

    def add_basis(self, reference: str) -> "RiskAssessmentBuilder":
        self._data.setdefault("basis", [])
        self._data["basis"].append({"reference": reference})
        return self
