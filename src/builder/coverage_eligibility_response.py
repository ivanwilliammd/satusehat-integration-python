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

    # Nama kanon. Modul ini memakai nama tanpa awalan (identifier, status, ...)
    # sementara 139 modul lain memakai set_/add_. Keduanya kini ada, yang lama
    # dipertahankan supaya pemanggil tidak pecah.
    def set_id(self, id: str) -> "CoverageEligibilityResponseBuilder":
        return self._set("id", id)

    def add_identifier(self, system: str, value: str) -> "CoverageEligibilityResponseBuilder":
        return self.identifier(system, value)

    def set_status(self, value: str) -> "CoverageEligibilityResponseBuilder":
        return self.status(value)

    def set_purpose(self, values: list) -> "CoverageEligibilityResponseBuilder":
        return self.purpose(values)

    def set_patient(self, reference: str, display: str = "") -> "CoverageEligibilityResponseBuilder":
        return self.patient(reference, display)

    def set_serviced_date(self, value: str) -> "CoverageEligibilityResponseBuilder":
        return self.serviced_date(value)

    def set_created(self, value: str) -> "CoverageEligibilityResponseBuilder":
        return self.created(value)

    def set_request(self, reference: str) -> "CoverageEligibilityResponseBuilder":
        return self.request(reference)

    def set_outcome(self, value: str) -> "CoverageEligibilityResponseBuilder":
        return self.outcome(value)

    def set_request_provider(self, reference: str) -> "CoverageEligibilityResponseBuilder":
        return self._set("requestProvider", {"reference": reference})

    def set_insurer(self, reference: str) -> "CoverageEligibilityResponseBuilder":
        return self._set("insurer", {"reference": reference})

    def add_coverage(self, reference: str, pre_auth_ref: str = "") -> "CoverageEligibilityResponseBuilder":
        coverage = {"reference": reference}
        if pre_auth_ref:
            coverage["preAuthRef"] = [pre_auth_ref]
        return self._push("coverage", coverage)

    def set_disposition(self, disposition: str) -> "CoverageEligibilityResponseBuilder":
        return self._set("disposition", disposition)

    def add_insurance(
        self,
        coverage_reference: str,
        benefit_balance_name: str = None,
        benefit_balance_type_system: str = None,
        benefit_balance_type_code: str = None,
        benefit_balance_type_display: str = None,
    ) -> "CoverageEligibilityResponseBuilder":
        insurance = {"coverage": {"reference": coverage_reference}}
        if benefit_balance_name:
            item = {"name": benefit_balance_name}
            if benefit_balance_type_system and benefit_balance_type_code:
                item["type"] = {
                    "coding": [
                        {
                            "system": benefit_balance_type_system,
                            "code": benefit_balance_type_code,
                            "display": benefit_balance_type_display or "",
                        }
                    ]
                }
            insurance["benefitBalance"] = [item]
        return self._push("insurance", insurance)

    def set_serviced_period(self, start: str, end: str = "") -> "CoverageEligibilityResponseBuilder":
        self._set("servicedPeriod/start", start)
        if end:
            self._set("servicedPeriod/end", end)
        return self
