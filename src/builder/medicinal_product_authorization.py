from src.builder.base_builder import BaseBuilder


class MedicinalProductAuthorizationBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("MedicinalProductAuthorization")

    def set_id(self, val: str) -> "MedicinalProductAuthorizationBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "MedicinalProductAuthorizationBuilder":
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

    def set_status(self, val: str) -> "MedicinalProductAuthorizationBuilder":
        return self._set("status", val)

    def set_country(self, system: str, code: str, display: str = "") -> "MedicinalProductAuthorizationBuilder":
        return self._set("country", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_regulator(self, ref: str, display: str = None) -> "MedicinalProductAuthorizationBuilder":
        return self._set("regulator", self._ref(ref, "Organization", display))

    def set_validity_period(self, val: str) -> "MedicinalProductAuthorizationBuilder":
        return self._set("validityPeriod", val)
