"""RiskAssessment resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class RiskAssessmentBuilder(BaseBuilder):
    """Builder for RiskAssessment resource."""

    def __init__(self):
        super().__init__("RiskAssessment")
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

    def add_identifier(self, system: str, value: str) -> "RiskAssessmentBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_code(self, konsep) -> "RiskAssessmentBuilder":
        return self._set("code", konsep)

    def set_performer(self, reference) -> "RiskAssessmentBuilder":
        return self._set("performer", reference if isinstance(reference, dict) else {"reference": reference})

    def add_reason_reference(self, reference) -> "RiskAssessmentBuilder":
        ref = reference if isinstance(reference, dict) else {"reference": reference}
        return self._push("reasonReference", ref)

    def add_extension(self, url: str, value, value_type: Optional[str] = None) -> "RiskAssessmentBuilder":
        ext = {"url": url}
        if value_type is not None:
            ext[f"value{value_type[0].upper()}{value_type[1:]}"] = value
        else:
            ext["valueString"] = value
        return self._push("extension", ext)

    def set_occurrence_date_time(self, value: str) -> "RiskAssessmentBuilder":
        """Elemen R4 bernama `occurrence[x]`; kanon menulis `occurrenceDateTime`."""
        return self.set_occurrence_datetime(value)
