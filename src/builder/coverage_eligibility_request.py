from src.builder.base_builder import BaseBuilder

class CoverageEligibilityRequestBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("CoverageEligibilityRequest")

    def identifier(self, system: str, value: str) -> "CoverageEligibilityRequestBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def status(self, value: str) -> "CoverageEligibilityRequestBuilder":
        return self._set("status", value)

    def priority(self, codeable_concept: dict) -> "CoverageEligibilityRequestBuilder":
        return self._set("priority", codeable_concept)

    def purpose(self, values: list) -> "CoverageEligibilityRequestBuilder":
        return self._set("purpose", values)

    def patient(self, reference: str, display: str = "") -> "CoverageEligibilityRequestBuilder":
        sub = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("patient", sub)

    def serviced_date(self, value: str) -> "CoverageEligibilityRequestBuilder":
        return self._set("servicedDate", value)

    def created(self, value: str) -> "CoverageEligibilityRequestBuilder":
        return self._set("created", value)

    def requestor(self, reference: str) -> "CoverageEligibilityRequestBuilder":
        return self._set("requestor", {"reference": reference})

    def insurer(self, reference: str) -> "CoverageEligibilityRequestBuilder":
        return self._set("insurer", {"reference": reference})
