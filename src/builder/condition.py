from typing import Any, Dict, List, Optional

from src.builder.base_builder import BaseBuilder


class ConditionBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Condition")

    def add_identifier(self, system: str, value: str) -> "ConditionBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append({"system": system, "value": value})
        return self

    def set_clinical_status(
        self,
        code: str,
        display: Optional[str] = None,
    ) -> "ConditionBuilder":
        self.data["clinicalStatus"] = {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": code,
                "display": display,
            }]
        }
        return self

    def set_verification_status(
        self,
        code: str,
        display: Optional[str] = None,
    ) -> "ConditionBuilder":
        self.data["verificationStatus"] = {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": code,
                "display": display,
            }]
        }
        return self

    def add_category(
        self,
        code: str,
        display: str,
        system: str = "http://terminology.hl7.org/CodeSystem/condition-category",
    ) -> "ConditionBuilder":
        if "category" not in self.data:
            self.data["category"] = []
        self.data["category"].append({
            "coding": [{"system": system, "code": code, "display": display}]
        })
        return self

    def set_severity(
        self,
        code: str,
        display: str,
    ) -> "ConditionBuilder":
        self.data["severity"] = {
            "coding": [{"code": code, "display": display}]
        }
        return self

    def set_code(
        self,
        code: str,
        display: str,
        system: str = "http://snomed.info/sct",
    ) -> "ConditionBuilder":
        self.data["code"] = {
            "coding": [{"system": system, "code": code, "display": display}]
        }
        return self

    def set_subject(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ConditionBuilder":
        subj: Dict[str, Any] = {"reference": reference}
        if display:
            subj["display"] = display
        self.data["subject"] = subj
        return self

    def set_encounter(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ConditionBuilder":
        enc: Dict[str, Any] = {"reference": reference}
        if display:
            enc["display"] = display
        self.data["encounter"] = enc
        return self

    def set_onset(self, onset: str) -> "ConditionBuilder":
        self.data["onsetDateTime"] = onset
        return self

    def set_abatement(self, abatement: str) -> "ConditionBuilder":
        self.data["abatementDateTime"] = abatement
        return self

    def set_recorded_date(self, recorded_date: str) -> "ConditionBuilder":
        self.data["recordedDate"] = recorded_date
        return self

    def set_recorder(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ConditionBuilder":
        rec: Dict[str, Any] = {"reference": reference}
        if display:
            rec["display"] = display
        self.data["recorder"] = rec
        return self

    def set_asserter(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ConditionBuilder":
        ass: Dict[str, Any] = {"reference": reference}
        if display:
            ass["display"] = display
        self.data["asserter"] = ass
        return self

    def add_stage(
        self,
        summary_code: str,
        summary_display: str,
        assessment_ref: Optional[str] = None,
    ) -> "ConditionBuilder":
        if "stage" not in self.data:
            self.data["stage"] = []
        stage: Dict[str, Any] = {
            "summary": {
                "coding": [{"code": summary_code, "display": summary_display}]
            }
        }
        if assessment_ref:
            stage["assessment"] = {"reference": assessment_ref}
        self.data["stage"].append(stage)
        return self

    def add_note(
        self,
        text: str,
        author_ref: Optional[str] = None,
    ) -> "ConditionBuilder":
        if "note" not in self.data:
            self.data["note"] = []
        note: Dict[str, Any] = {"text": text}
        if author_ref:
            note["authorReference"] = {"reference": author_ref}
        self.data["note"].append(note)
        return self
