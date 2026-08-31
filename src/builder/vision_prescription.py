from src.builder.base_builder import BaseBuilder


class VisionPrescriptionBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("VisionPrescription")

    def set_id(self, val: str) -> "VisionPrescriptionBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "VisionPrescriptionBuilder":
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

    def set_status(self, val: str) -> "VisionPrescriptionBuilder":
        return self._set("status", val)

    def set_code(self, system: str, code: str, display: str) -> "VisionPrescriptionBuilder":
        return self._set("code", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_subject(self, ref: str, display: str = None) -> "VisionPrescriptionBuilder":
        return self._set("subject", self._ref(ref, "Patient", display))

    def set_encounter(self, ref: str, display: str = None) -> "VisionPrescriptionBuilder":
        return self._set("encounter", self._ref(ref, "Encounter", display))
