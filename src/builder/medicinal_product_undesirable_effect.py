from src.builder.base_builder import BaseBuilder


class MedicinalProductUndesirableEffectBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("MedicinalProductUndesirableEffect")

    def set_id(self, val: str) -> "MedicinalProductUndesirableEffectBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "MedicinalProductUndesirableEffectBuilder":
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

    def set_status(self, val: str) -> "MedicinalProductUndesirableEffectBuilder":
        return self._set("status", val)

    def set_subject(self, ref: str, display: str = None) -> "MedicinalProductUndesirableEffectBuilder":
        return self._set("subject", self._ref(ref, "Patient", display))

    def set_symptom_condition_effect(self, system: str, code: str, display: str = "") -> "MedicinalProductUndesirableEffectBuilder":
        return self._set("symptomConditionEffect", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_classification(self, system: str, code: str, display: str = "") -> "MedicinalProductUndesirableEffectBuilder":
        return self._set("classification", {"coding": [{"system": system, "code": code, "display": display}]})
