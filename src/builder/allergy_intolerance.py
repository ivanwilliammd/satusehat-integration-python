from src.builder.base_builder import BaseBuilder

class AllergyIntoleranceBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("AllergyIntoleranceBuilder")

    def identifier(self, identifier: dict) -> "AllergyIntoleranceBuilder":
        return self._push("identifier", identifier)

    def clinical_status(self, code: str, system: str = "http://terminology.kemkes.go.id/CodeSystem/allergyintolerance-clinical", display: str = "") -> "AllergyIntoleranceBuilder":
        v = {"coding": [{"system": system, "code": code, "display": display}]}
        return self._set("clinicalStatus", v)

    def verification_status(self, code: str, system: str = "http://terminology.kemkes.go.id/CodeSystem/allergyintolerance-verification", display: str = "") -> "AllergyIntoleranceBuilder":
        return self._set("verificationStatus", {"coding": [{"system": system, "code": code, "display": display}]})

    def type(self, code: str, system: str = "http://terminology.kemkes.go.id/CodeSystem/allergyintolerance-type", display: str = "") -> "AllergyIntoleranceBuilder":
        return self._set("type", {"coding": [{"system": system, "code": code, "display": display}]})

    def category(self, value: str) -> "AllergyIntoleranceBuilder":
        return self._set("category", [value])

    def code(self, codeable_concept: dict) -> "AllergyIntoleranceBuilder":
        return self._set("code", codeable_concept)

    def patient(self, reference: str, display: str = "") -> "AllergyIntoleranceBuilder":
        sub = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("patient", sub)

    def encounter(self, reference: str) -> "AllergyIntoleranceBuilder":
        return self._set("encounter", {"reference": reference})

    def onset_date_time(self, value: str) -> "AllergyIntoleranceBuilder":
        return self._set("onsetDateTime", value)

    def recorded_date(self, value: str) -> "AllergyIntoleranceBuilder":
        return self._set("recordedDate", value)

    def recorder(self, reference: str) -> "AllergyIntoleranceBuilder":
        return self._set("recorder", {"reference": reference})

    def asserter(self, reference: str) -> "AllergyIntoleranceBuilder":
        return self._set("asserter", {"reference": reference})

    def note(self, text: str) -> "AllergyIntoleranceBuilder":
        return self._set("note", [{"text": text}])
