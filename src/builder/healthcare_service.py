from src.builder.base_builder import BaseBuilder


class HealthcareServiceBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("HealthcareService")

    def set_id(self, val: str) -> "HealthcareServiceBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "HealthcareServiceBuilder":
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

    def set_status(self, val: str) -> "HealthcareServiceBuilder":
        return self._set("status", val)

    def set_name(self, val: str) -> "HealthcareServiceBuilder":
        return self._set("name", val)

    def set_type(self, system: str, code: str, display: str = "") -> "HealthcareServiceBuilder":
        return self._set("type", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_location(self, ref: str, display: str = None) -> "HealthcareServiceBuilder":
        return self._set("location", self._ref(ref, "Location", display))

    def set_provided_by(self, ref: str, display: str = None) -> "HealthcareServiceBuilder":
        return self._set("providedBy", self._ref(ref, "Organization", display))
