from src.builder.base_builder import BaseBuilder


class EnrollmentResponseBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("EnrollmentResponse")

    def set_id(self, val: str) -> "EnrollmentResponseBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "EnrollmentResponseBuilder":
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

    def set_status(self, val: str) -> "EnrollmentResponseBuilder":
        return self._set("status", val)

    def set_request(self, ref: str, display: str = None) -> "EnrollmentResponseBuilder":
        result = {"reference": ref}
        if display:
            result["display"] = display
        return self._set("request", result)

    def set_outcome(self, system: str, code: str, display: str = "") -> "EnrollmentResponseBuilder":
        return self._set("outcome", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_disposition(self, val: str) -> "EnrollmentResponseBuilder":
        return self._set("disposition", val)

    def set_created(self, val: str) -> "EnrollmentResponseBuilder":
        return self._set("created", val)
