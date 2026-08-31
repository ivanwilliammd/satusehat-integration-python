from src.builder.base_builder import BaseBuilder


class MedicinalProductInteractionBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("MedicinalProductInteraction")

    def set_id(self, val: str) -> "MedicinalProductInteractionBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "MedicinalProductInteractionBuilder":
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

    def set_status(self, val: str) -> "MedicinalProductInteractionBuilder":
        return self._set("status", val)

    def set_subject(self, ref: str, display: str = None) -> "MedicinalProductInteractionBuilder":
        return self._set("subject", self._ref(ref, "Patient", display))

    def set_description(self, val: str) -> "MedicinalProductInteractionBuilder":
        return self._set("description", val)

    def set_interactant(self, system: str, code: str, display: str = "") -> "MedicinalProductInteractionBuilder":
        return self._set("interactant", {"coding": [{"system": system, "code": code, "display": display}]})
