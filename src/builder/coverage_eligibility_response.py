from src.builder.base_builder import BaseBuilder

class CoverageEligibilityResponseBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("CoverageEligibilityResponse")

    def identifier(self, system: str, value: str) -> "CoverageEligibilityResponseBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def status(self, value: str) -> "CoverageEligibilityResponseBuilder":
        return self._set("status", value)

    def purpose(self, values: list) -> "CoverageEligibilityResponseBuilder":
        return self._set("purpose", values)

    def patient(self, reference: str, display: str = "") -> "CoverageEligibilityResponseBuilder":
        sub = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("patient", sub)

    def serviced_date(self, value: str) -> "CoverageEligibilityResponseBuilder":
        return self._set("servicedDate", value)

    def created(self, value: str) -> "CoverageEligibilityResponseBuilder":
        return self._set("created", value)

    def request(self, reference: str) -> "CoverageEligibilityResponseBuilder":
        return self._set("request", {"reference": reference})

    def outcome(self, value: str) -> "CoverageEligibilityResponseBuilder":
        return self._set("outcome", value)
