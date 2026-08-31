from src.builder.base_builder import BaseBuilder


class OrganizationAffiliationBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("OrganizationAffiliation")

    def set_id(self, val: str) -> "OrganizationAffiliationBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "OrganizationAffiliationBuilder":
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

    def set_status(self, val: str) -> "OrganizationAffiliationBuilder":
        return self._set("status", val)

    def set_organization(self, ref: str, display: str = None) -> "OrganizationAffiliationBuilder":
        return self._set("organization", self._ref(ref, "Organization", display))

    def set_participating_organization(self, ref: str, display: str = None) -> "OrganizationAffiliationBuilder":
        return self._set("participatingOrganization", self._ref(ref, "Organization", display))

    def set_network(self, system: str, code: str, display: str = "") -> "OrganizationAffiliationBuilder":
        return self._set("network", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_code(self, system: str, code: str, display: str = "") -> "OrganizationAffiliationBuilder":
        return self._set("code", {"coding": [{"system": system, "code": code, "display": display}]})
