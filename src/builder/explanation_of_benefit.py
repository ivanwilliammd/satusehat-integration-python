from src.builder.base_builder import BaseBuilder


class ExplanationOfBenefitBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ExplanationOfBenefit")

    def set_id(self, val: str) -> "ExplanationOfBenefitBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "ExplanationOfBenefitBuilder":
        ident = {"system": system, "value": value}
        if use:
            ident["use"] = use
        if type_code:
            ident["type"] = {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                    "code": type_code,
                    "display": type_display if type_display else type_code,
                }]
            }
        return self._push("identifier", ident)

    def set_status(self, val: str) -> "ExplanationOfBenefitBuilder":
        return self._set("status", val)

    def set_type(self, system: str, code: str, display: str = "") -> "ExplanationOfBenefitBuilder":
        return self._set("type", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_use(self, system: str, code: str, display: str = "") -> "ExplanationOfBenefitBuilder":
        return self._set("use", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_patient(self, ref: str, display: str = None) -> "ExplanationOfBenefitBuilder":
        return self._set("patient", self._ref(ref, "Patient", display))

    def set_created(self, val: str) -> "ExplanationOfBenefitBuilder":
        return self._set("created", val)

    def set_provider(self, ref: str, display: str = None) -> "ExplanationOfBenefitBuilder":
        return self._set("provider", self._ref(ref, "Practitioner", display))
