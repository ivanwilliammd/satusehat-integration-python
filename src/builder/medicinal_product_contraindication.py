from src.builder.base_builder import BaseBuilder


class MedicinalProductContraindicationBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("MedicinalProductContraindication")

    def set_id(self, val: str) -> "MedicinalProductContraindicationBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "MedicinalProductContraindicationBuilder":
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

    def set_status(self, val: str) -> "MedicinalProductContraindicationBuilder":
        return self._set("status", val)

    def set_subject(self, ref: str, display: str = None) -> "MedicinalProductContraindicationBuilder":
        return self._set("subject", self._ref(ref, "Patient", display))

    def set_disease(self, system: str, code: str, display: str = "") -> "MedicinalProductContraindicationBuilder":
        return self._set("disease", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_comorbidity(self, ref: str, display: str = None) -> "MedicinalProductContraindicationBuilder":
        result = {"reference": ref}
        if display:
            result["display"] = display
        return self._set("comorbidity", result)
