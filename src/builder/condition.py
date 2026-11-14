from typing import Any, Dict, List, Optional

from src.builder.base_builder import BaseBuilder


def _arr(value: Any) -> Any:
    return value.to_array() if hasattr(value, "to_array") else value


class ConditionBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Condition")

    def set_id(self, id: str) -> "ConditionBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "ConditionBuilder":
        if value is not None:
            return self._push("identifier", {"system": identifier, "value": value})
        return self._push("identifier", _arr(identifier))

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
        summary: Any,
        summary_display: Optional[str] = None,
        assessment: Any = None,
    ) -> "ConditionBuilder":
        # FHIR R4: stage.assessment adalah 0..* Reference, jadi selalu ditulis sebagai list.
        if isinstance(summary, str):
            ringkas: Dict[str, Any] = {"coding": [{"code": summary, "display": summary_display or summary}]}
        else:
            ringkas = _arr(summary)
        stage: Dict[str, Any] = {"summary": ringkas}
        if assessment is not None:
            if isinstance(assessment, str):
                stage["assessment"] = [{"reference": assessment}]
            elif isinstance(assessment, list):
                stage["assessment"] = [_arr(a) for a in assessment]
            else:
                stage["assessment"] = [_arr(assessment)]
        return self._push("stage", stage)

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

    # onset[x] dan abatement[x] lengkap, sesuai PayloadBuilderCondition.
    def set_onset_date_time(self, date_time: str) -> "ConditionBuilder":
        self.data["onsetDateTime"] = date_time
        return self

    def set_onset_age(self, age: Any) -> "ConditionBuilder":
        self.data["onsetAge"] = _arr(age)
        return self

    def set_onset_period(self, period: Any) -> "ConditionBuilder":
        self.data["onsetPeriod"] = _arr(period)
        return self

    def set_onset_range(self, onset_range: Any) -> "ConditionBuilder":
        self.data["onsetRange"] = _arr(onset_range)
        return self

    def set_onset_string(self, onset_string: str) -> "ConditionBuilder":
        self.data["onsetString"] = onset_string
        return self

    def set_abatement_date_time(self, date_time: str) -> "ConditionBuilder":
        self.data["abatementDateTime"] = date_time
        return self

    def set_abatement_age(self, age: Any) -> "ConditionBuilder":
        self.data["abatementAge"] = _arr(age)
        return self

    def set_abatement_period(self, period: Any) -> "ConditionBuilder":
        self.data["abatementPeriod"] = _arr(period)
        return self

    def set_abatement_range(self, abatement_range: Any) -> "ConditionBuilder":
        self.data["abatementRange"] = _arr(abatement_range)
        return self

    def set_abatement_string(self, abatement_string: str) -> "ConditionBuilder":
        self.data["abatementString"] = abatement_string
        return self

    def add_evidence(self, code: Any, detail: Any = None) -> "ConditionBuilder":
        evidence: Dict[str, Any] = {"code": [_arr(code)]}
        if detail is not None:
            evidence["detail"] = [_arr(detail)]
        return self._push("evidence", evidence)

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "ConditionBuilder":
        extension: Dict[str, Any] = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        return self._push("extension", extension)
