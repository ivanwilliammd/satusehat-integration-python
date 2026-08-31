from src.builder.base_builder import BaseBuilder


class ResourceGuideBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ResourceGuide")

    def set_id(self, val: str) -> "ResourceGuideBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "ResourceGuideBuilder":
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

    def set_status(self, val: str) -> "ResourceGuideBuilder":
        return self._set("status", val)

    def set_name(self, val: str) -> "ResourceGuideBuilder":
        return self._set("name", val)

    def set_description(self, val: str) -> "ResourceGuideBuilder":
        return self._set("description", val)

    def set_version(self, val: str) -> "ResourceGuideBuilder":
        return self._set("version", val)

    def set_publisher(self, val: str) -> "ResourceGuideBuilder":
        return self._set("publisher", val)
