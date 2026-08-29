"""RiskAssessment resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class RiskAssessmentBuilder(BaseBuilder):
    """Builder for RiskAssessment resource."""

    def __init__(self):
        super().__init__("RiskAssessmentBuilder")
        self.data = {"resourceType": "RiskAssessment"}

    def set_id(self, id: str) -> "RiskAssessmentBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "RiskAssessmentBuilder":
        self.data["status"] = status
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "RiskAssessmentBuilder":
        self.data["subject"] = {"reference": reference}
        if display:
            self.data["subject"]["display"] = display
        return self

    def set_encounter(self, reference: str) -> "RiskAssessmentBuilder":
        self.data["encounter"] = {"reference": reference}
        return self

    def set_occurrence_datetime(self, occurrence_datetime: str) -> "RiskAssessmentBuilder":
        self.data["occurrenceDateTime"] = occurrence_datetime
        return self

    def set_condition(self, reference: str, display: Optional[str] = None) -> "RiskAssessmentBuilder":
        self.data["condition"] = {"reference": reference}
        if display:
            self.data["condition"]["display"] = display
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
        self.data.setdefault("prediction", [])
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
        self.data["prediction"].append(pred)
        return self

    def set_mitigation(self, mitigation: str) -> "RiskAssessmentBuilder":
        self.data["mitigation"] = mitigation
        return self

    def add_note(self, text: str) -> "RiskAssessmentBuilder":
        self.data.setdefault("note", [])
        self.data["note"].append({"text": text})
        return self

    def add_basis(self, reference: str) -> "RiskAssessmentBuilder":
        self.data.setdefault("basis", [])
        self.data["basis"].append({"reference": reference})
        return self
