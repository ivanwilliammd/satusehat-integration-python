from typing import Any, Dict, List, Optional

from src.builder.base_builder import BaseBuilder


class ProcedureBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Procedure")

    def add_identifier(self, system: str, value: str) -> "ProcedureBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append({"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "ProcedureBuilder":
        self.data["status"] = status
        return self

    def set_category(
        self,
        code: str,
        display: str,
        system: str = "http://snomed.info/sct",
    ) -> "ProcedureBuilder":
        self.data["category"] = {
            "coding": [{"system": system, "code": code, "display": display}]
        }
        return self

    def set_code(
        self,
        code: str,
        display: str,
        system: str = "http://snomed.info/sct",
    ) -> "ProcedureBuilder":
        self.data["code"] = {
            "coding": [{"system": system, "code": code, "display": display}]
        }
        return self

    def set_subject(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ProcedureBuilder":
        subj: Dict[str, Any] = {"reference": reference}
        if display:
            subj["display"] = display
        self.data["subject"] = subj
        return self

    def set_encounter(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ProcedureBuilder":
        enc: Dict[str, Any] = {"reference": reference}
        if display:
            enc["display"] = display
        self.data["encounter"] = enc
        return self

    def set_performed(self, performed: str) -> "ProcedureBuilder":
        self.data["performedDateTime"] = performed
        return self

    def set_performed_period(
        self,
        start: str,
        end: str,
    ) -> "ProcedureBuilder":
        self.data["performedPeriod"] = {"start": start, "end": end}
        return self

    def set_reporter(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ProcedureBuilder":
        rep: Dict[str, Any] = {"reference": reference}
        if display:
            rep["display"] = display
        self.data["reporter"] = rep
        return self

    def add_performer(
        self,
        reference: str,
        display: Optional[str] = None,
        role_code: Optional[str] = None,
        role_display: Optional[str] = None,
    ) -> "ProcedureBuilder":
        if "performer" not in self.data:
            self.data["performer"] = []
        entry: Dict[str, Any] = {"individual": {"reference": reference}}
        if display:
            entry["individual"]["display"] = display
        if role_code:
            entry["function"] = {
                "coding": [{"code": role_code, "display": role_display}]
            }
        self.data["performer"].append(entry)
        return self

    def set_location(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "ProcedureBuilder":
        loc: Dict[str, Any] = {"reference": reference}
        if display:
            loc["display"] = display
        self.data["location"] = loc
        return self

    def add_reason(
        self,
        code: str,
        display: str,
        system: str = "http://snomed.info/sct",
    ) -> "ProcedureBuilder":
        if "reasonCode" not in self.data:
            self.data["reasonCode"] = []
        self.data["reasonCode"].append({
            "coding": [{"system": system, "code": code, "display": display}]
        })
        return self

    def set_outcome(
        self,
        code: str,
        display: str,
    ) -> "ProcedureBuilder":
        self.data["outcome"] = {
            "coding": [{"code": code, "display": display}]
        }
        return self

    def add_complication(
        self,
        code: str,
        display: str,
        system: str = "http://snomed.info/sct",
    ) -> "ProcedureBuilder":
        if "complication" not in self.data:
            self.data["complication"] = []
        self.data["complication"].append({
            "coding": [{"system": system, "code": code, "display": display}]
        })
        return self

    def add_body_site(
        self,
        code: str,
        display: str,
        system: str = "http://snomed.info/sct",
    ) -> "ProcedureBuilder":
        if "bodySite" not in self.data:
            self.data["bodySite"] = []
        self.data["bodySite"].append({
            "coding": [{"system": system, "code": code, "display": display}]
        })
        return self
