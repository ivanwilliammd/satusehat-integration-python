from src.builder.base_builder import BaseBuilder

class ClinicalImpressionBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ClinicalImpressionBuilder")

    def identifier(self, identifier: dict) -> "ClinicalImpressionBuilder":
        return self._push("identifier", identifier)

    def status(self, value: str) -> "ClinicalImpressionBuilder":
        return self._set("status", value)

    def code(self, codeable_concept: dict) -> "ClinicalImpressionBuilder":
        return self._set("code", codeable_concept)

    def subject(self, reference: str, display: str = "") -> "ClinicalImpressionBuilder":
        sub = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("subject", sub)

    def encounter(self, reference: str) -> "ClinicalImpressionBuilder":
        return self._set("encounter", {"reference": reference})

    def effective_date_time(self, value: str) -> "ClinicalImpressionBuilder":
        return self._set("effectiveDateTime", value)

    def effective_period(self, period: dict) -> "ClinicalImpressionBuilder":
        return self._set("effectivePeriod", period)

    def date(self, value: str) -> "ClinicalImpressionBuilder":
        return self._set("date", value)

    def assessor(self, reference: str) -> "ClinicalImpressionBuilder":
        return self._set("assessor", {"reference": reference})

    def note(self, text: str) -> "ClinicalImpressionBuilder":
        return self._set("note", [{"text": text}])
