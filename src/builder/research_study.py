from src.builder.base_builder import BaseBuilder


class ResearchStudyBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ResearchStudy")

    def set_id(self, val: str) -> "ResearchStudyBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "ResearchStudyBuilder":
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

    def set_status(self, val: str) -> "ResearchStudyBuilder":
        return self._set("status", val)

    def set_title(self, val: str) -> "ResearchStudyBuilder":
        return self._set("title", val)

    def set_protocol(self, ref: str, display: str = None) -> "ResearchStudyBuilder":
        result = {"reference": ref}
        if display:
            result["display"] = display
        return self._set("protocol", result)

    def set_sponsor(self, ref: str, display: str = None) -> "ResearchStudyBuilder":
        return self._set("sponsor", self._ref(ref, "Organization", display))

    def set_phase(self, system: str, code: str, display: str = "") -> "ResearchStudyBuilder":
        return self._set("phase", {"coding": [{"system": system, "code": code, "display": display}]})
