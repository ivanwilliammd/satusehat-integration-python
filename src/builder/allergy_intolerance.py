from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class AllergyIntoleranceBuilder(BaseBuilder):
    _resourceType = "AllergyIntolerance"

    def __init__(self) -> None:
        super().__init__("AllergyIntoleranceBuilder")

    def clinical_status(self, code: str, system: str = "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical") -> "AllergyIntoleranceBuilder":
        return self._set("clinicalStatus", {"coding": [{"code": code, "system": system}]})

    def verification_status(self, code: str, system: str = "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification") -> "AllergyIntoleranceBuilder":
        return self._set("verificationStatus", {"coding": [{"code": code, "system": system}]})

    def type(self, value: str) -> "AllergyIntoleranceBuilder":
        return self._set("type", value)

    def category(self, value: str) -> "AllergyIntoleranceBuilder":
        return self._set("category", value)

    def criticality(self, value: str) -> "AllergyIntoleranceBuilder":
        return self._set("criticality", value)

    def code(self, codeable_concept: dict) -> "AllergyIntoleranceBuilder":
        return self._set("code", codeable_concept)

    def patient(self, reference: str, display: Optional[str] = None) -> "AllergyIntoleranceBuilder":
        pt: dict = {"reference": reference}
        if display:
            pt["display"] = display
        return self._set("patient", pt)

    def encounter(self, reference: str) -> "AllergyIntoleranceBuilder":
        return self._set("encounter", {"reference": reference})

    def onset_date_time(self, value: str) -> "AllergyIntoleranceBuilder":
        return self._set("onsetDateTime", value)

    def recorded_date(self, value: str) -> "AllergyIntoleranceBuilder":
        return self._set("recordedDate", value)

    def recorder(self, reference: str, display: Optional[str] = None) -> "AllergyIntoleranceBuilder":
        rec: dict = {"reference": reference}
        if display:
            rec["display"] = display
        return self._set("recorder", rec)

    def asserter(self, reference: str, display: Optional[str] = None) -> "AllergyIntoleranceBuilder":
        ast: dict = {"reference": reference}
        if display:
            ast["display"] = display
        return self._set("asserter", ast)

    def reaction(self, substance: Optional[dict] = None, manifestation: Optional[List[dict]] = None, description: Optional[str] = None, onset: Optional[str] = None, severity: Optional[str] = None, note: Optional[str] = None) -> "AllergyIntoleranceBuilder":
        rxn: dict = {}
        if substance:
            rxn["substance"] = substance
        if manifestation:
            rxn["manifestation"] = manifestation
        if description:
            rxn["description"] = description
        if onset:
            rxn["onset"] = onset
        if severity:
            rxn["severity"] = severity
        if note:
            rxn["note"] = [{"text": note}]
        return self._append("reaction", rxn) if rxn else self
