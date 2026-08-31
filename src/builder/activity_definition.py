from src.builder.base_builder import BaseBuilder


class ActivityDefinitionBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ActivityDefinition")

    def set_id(self, val: str) -> "ActivityDefinitionBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "ActivityDefinitionBuilder":
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

    def set_status(self, val: str) -> "ActivityDefinitionBuilder":
        return self._set("status", val)

    def set_description(self, val: str) -> "ActivityDefinitionBuilder":
        return self._set("description", val)

    def set_kind(self, system: str, code: str, display: str = "") -> "ActivityDefinitionBuilder":
        return self._set("kind", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_code(self, system: str, code: str, display: str = "") -> "ActivityDefinitionBuilder":
        return self._set("code", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_author(self, ref: str, display: str = None) -> "ActivityDefinitionBuilder":
        return self._set("author", self._ref(ref, "Practitioner", display))

    def set_timing(self, val: str) -> "ActivityDefinitionBuilder":
        return self._set("timing", val)
