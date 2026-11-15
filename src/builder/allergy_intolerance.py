from typing import Any, Optional
from src.builder.base_builder import BaseBuilder

class AllergyIntoleranceBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("AllergyIntolerance")

    def identifier(self, identifier: dict) -> "AllergyIntoleranceBuilder":
        return self._push("identifier", identifier)

    def clinical_status(self, system: str = "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical", code: str = "", display: str = "") -> "AllergyIntoleranceBuilder":
        v = {"coding": [{"system": system, "code": code, "display": display}]}
        return self._set("clinicalStatus", v)

    def verification_status(self, system: str = "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification", code: str = "", display: str = "") -> "AllergyIntoleranceBuilder":
        return self._set("verificationStatus", {"coding": [{"system": system, "code": code, "display": display}]})

    def type(self, system: str = "http://hl7.org/fhir/allergy-intolerance-type", code: str = "", display: str = "") -> "AllergyIntoleranceBuilder":
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

    # --- Nama kanon (cermin PayloadBuilderAllergyIntolerance) ---

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "AllergyIntoleranceBuilder":
        if value is not None:
            entry: dict = {"system": identifier, "value": value}
        else:
            entry = identifier.to_array() if hasattr(identifier, "to_array") else identifier
        self.data.setdefault("identifier", []).append(entry)
        return self

    def set_clinical_status(self, status: str) -> "AllergyIntoleranceBuilder":
        self.data["clinicalStatus"] = {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical", "code": status}]
        }
        return self

    def set_verification_status(self, status: str) -> "AllergyIntoleranceBuilder":
        self.data["verificationStatus"] = {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification", "code": status}]
        }
        return self

    def set_type(self, allergy_type: str) -> "AllergyIntoleranceBuilder":
        self.data["type"] = allergy_type
        return self

    def add_category(self, category: str) -> "AllergyIntoleranceBuilder":
        self.data.setdefault("category", []).append(category)
        return self

    def set_criticality(self, criticality: str) -> "AllergyIntoleranceBuilder":
        self.data["criticality"] = criticality
        return self

    def set_code(self, code: Any) -> "AllergyIntoleranceBuilder":
        self.data["code"] = code.to_array() if hasattr(code, "to_array") else code
        return self

    def set_patient(self, patient: Any, display: Optional[str] = None) -> "AllergyIntoleranceBuilder":
        if isinstance(patient, str):
            ref: dict = {"reference": patient}
            if display:
                ref["display"] = display
            self.data["patient"] = ref
        else:
            self.data["patient"] = patient.to_array() if hasattr(patient, "to_array") else patient
        return self

    def set_encounter(self, encounter: Any) -> "AllergyIntoleranceBuilder":
        self.data["encounter"] = {"reference": encounter} if isinstance(encounter, str) else (
            encounter.to_array() if hasattr(encounter, "to_array") else encounter
        )
        return self

    def set_onset_date_time(self, date_time: str) -> "AllergyIntoleranceBuilder":
        self.data["onsetDateTime"] = date_time
        return self

    def set_recorded_date(self, date_time: str) -> "AllergyIntoleranceBuilder":
        self.data["recordedDate"] = date_time
        return self

    def set_recorder(self, recorder: Any, display: Optional[str] = None) -> "AllergyIntoleranceBuilder":
        if isinstance(recorder, str):
            ref: dict = {"reference": recorder}
            if display:
                ref["display"] = display
            self.data["recorder"] = ref
        else:
            self.data["recorder"] = recorder.to_array() if hasattr(recorder, "to_array") else recorder
        return self

    def set_asserter(self, asserter: Any, display: Optional[str] = None) -> "AllergyIntoleranceBuilder":
        if isinstance(asserter, str):
            ref: dict = {"reference": asserter}
            if display:
                ref["display"] = display
            self.data["asserter"] = ref
        else:
            self.data["asserter"] = asserter.to_array() if hasattr(asserter, "to_array") else asserter
        return self

    def set_last_occurrence(self, date_time: str) -> "AllergyIntoleranceBuilder":
        self.data["lastOccurrence"] = date_time
        return self

    def add_note(self, note: str) -> "AllergyIntoleranceBuilder":
        self.data.setdefault("note", []).append({"text": note})
        return self

    def add_reaction(self, substance: Any, manifestation: Any, description: Optional[str] = None,
                     onset: Optional[str] = None, severity: Optional[str] = None,
                     exposure_route: Any = None, note: Optional[str] = None) -> "AllergyIntoleranceBuilder":
        arr = lambda v: v.to_array() if hasattr(v, "to_array") else v
        reaction: dict = {"substance": arr(substance), "manifestation": [arr(manifestation)]}
        if description is not None:
            reaction["description"] = description
        if onset is not None:
            reaction["onset"] = onset
        if severity is not None:
            reaction["severity"] = severity
        if exposure_route is not None:
            reaction["exposureRoute"] = arr(exposure_route)
        if note is not None:
            reaction["note"] = [{"text": note}]
        self.data.setdefault("reaction", []).append(reaction)
        return self
