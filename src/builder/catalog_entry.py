from src.builder.base_builder import BaseBuilder


class CatalogEntryBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("CatalogEntry")

    def set_id(self, val: str) -> "CatalogEntryBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "CatalogEntryBuilder":
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

    def set_status(self, val: str) -> "CatalogEntryBuilder":
        return self._set("status", val)

    def set_type(self, system: str, code: str, display: str = "") -> "CatalogEntryBuilder":
        return self._set("type", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_reference(self, ref: str, display: str = None) -> "CatalogEntryBuilder":
        result = {"reference": ref}
        if display:
            result["display"] = display
        return self._set("reference", result)

    def set_validity_period(self, val: str) -> "CatalogEntryBuilder":
        return self._set("validityPeriod", val)
