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
    # Nama kanon; lihat catatan di coverage_eligibility_response.py.
    def set_id(self, id: str) -> "CoverageEligibilityRequestBuilder":
        return self._set("id", id)

    def add_identifier(self, system: str, value: str) -> "CoverageEligibilityRequestBuilder":
        return self.identifier(system, value)

    def set_status(self, value: str) -> "CoverageEligibilityRequestBuilder":
        return self.status(value)

    def set_priority(self, *args) -> "CoverageEligibilityRequestBuilder":
        """Menerima tiga argumen (system, code, display) seperti PHP, atau satu dict."""
        if len(args) == 1 and isinstance(args[0], dict):
            return self.priority(args[0])
        system, code, display = args
        return self.priority({"coding": [{"system": system, "code": code, "display": display}]})

    def set_purpose(self, values: list) -> "CoverageEligibilityRequestBuilder":
        return self.purpose(values)

    def set_patient(self, reference: str, display: str = "") -> "CoverageEligibilityRequestBuilder":
        return self.patient(reference, display)

    def set_serviced_date(self, value: str) -> "CoverageEligibilityRequestBuilder":
        return self.serviced_date(value)

    def set_created(self, value: str) -> "CoverageEligibilityRequestBuilder":
        return self.created(value)

    def set_requestor(self, reference: str) -> "CoverageEligibilityRequestBuilder":
        return self.requestor(reference)

    def set_insurer(self, reference: str) -> "CoverageEligibilityRequestBuilder":
        return self.insurer(reference)

    def set_enterer(self, reference: str) -> "CoverageEligibilityRequestBuilder":
        return self._set("enterer", {"reference": reference})

    def set_provider(self, reference: str) -> "CoverageEligibilityRequestBuilder":
        return self._set("provider", {"reference": reference})

    def add_coverage(self, reference: str, pre_auth_ref: str = "") -> "CoverageEligibilityRequestBuilder":
        coverage = {"reference": reference}
        if pre_auth_ref:
            coverage["preAuthRef"] = [pre_auth_ref]
        return self._push("coverage", coverage)

    def add_item(
        self,
        product_or_service_system: str,
        product_or_service_code: str,
        product_or_service_display: str,
        category_system: str = None,
        category_code: str = None,
    ) -> "CoverageEligibilityRequestBuilder":
        item = {
            "productOrService": {
                "coding": [
                    {
                        "system": product_or_service_system,
                        "code": product_or_service_code,
                        "display": product_or_service_display,
                    }
                ]
            }
        }
        if category_system and category_code:
            item["category"] = {"coding": [{"system": category_system, "code": category_code}]}
        return self._push("item", item)
