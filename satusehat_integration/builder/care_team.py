from typing import Optional
from satusehat_integration.builder.base_builder import BaseBuilder


class CareTeamBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("CareTeam")

    def set_id(self, id: str) -> "CareTeamBuilder":
        self._set("id", id)
        return self

    def add_identifier(
        self,
        system: str,
        value: str,
        use: str = None,
        type_code: str = None,
        type_display: str = None,
    ) -> "CareTeamBuilder":
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
        self._append("identifier", ident)
        return self

    def set_status(self, status: str) -> "CareTeamBuilder":
        self._set("status", status)
        return self

    def set_code(self, code: dict) -> "CareTeamBuilder":
        self._set("code", code)
        return self

    def set_subject(self, reference: str, display: str = None) -> "CareTeamBuilder":
        self._set("subject", {"reference": reference, "display": display}) if display else self._set("subject", {"reference": reference})
        return self

    def set_description(self, description: str) -> "CareTeamBuilder":
        self._set("description", description)
        return self

    def set_encounter(self, reference: str) -> "CareTeamBuilder":
        return self._set("encounter", {"reference": reference})
