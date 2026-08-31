from src.builder.base_builder import BaseBuilder


class CapabilityStatementBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("CapabilityStatement")

    def set_id(self, val: str) -> "CapabilityStatementBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "CapabilityStatementBuilder":
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

    def set_status(self, val: str) -> "CapabilityStatementBuilder":
        return self._set("status", val)

    def set_date(self, val: str) -> "CapabilityStatementBuilder":
        return self._set("date", val)

    def set_kind(self, system: str, code: str, display: str = "") -> "CapabilityStatementBuilder":
        return self._set("kind", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_fhir_version(self, system: str, code: str, display: str = "") -> "CapabilityStatementBuilder":
        return self._set("fhirVersion", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_format(self, system: str, code: str, display: str = "") -> "CapabilityStatementBuilder":
        return self._set("format", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_rest(self, system: str, code: str, display: str = "") -> "CapabilityStatementBuilder":
        return self._set("rest", {"coding": [{"system": system, "code": code, "display": display}]})
