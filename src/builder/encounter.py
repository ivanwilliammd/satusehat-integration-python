from typing import Any, Dict, List, Optional

from src.datatype.datatypes import Identifier
from src.builder.base_builder import BaseBuilder


class EncounterBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Encounter")

    def add_identifier(self, identifier: Identifier) -> "EncounterBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append(identifier.to_array())
        return self

    def set_status(self, status: str) -> "EncounterBuilder":
        self.data["status"] = status
        return self

    def set_class(
        self,
        class_code: str,
        display: Optional[str] = None,
        system: str = "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    ) -> "EncounterBuilder":
        self.data["class"] = {
            "system": system,
            "code": class_code,
            "display": display,
        }
        return self

    def set_subject(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "EncounterBuilder":
        subj: Dict[str, Any] = {"reference": reference}
        if display:
            subj["display"] = display
        self.data["subject"] = subj
        return self

    def add_participant(
        self,
        reference: str,
        display: Optional[str] = None,
        individual_type: Optional[str] = None,
        individual_code: Optional[str] = None,
        individual_display: Optional[str] = None,
    ) -> "EncounterBuilder":
        if "participant" not in self.data:
            self.data["participant"] = []
        entry: Dict[str, Any] = {}
        if individual_type and individual_code:
            entry["type"] = [{
                "coding": [{
                    "system": individual_type,
                    "code": individual_code,
                    "display": individual_display,
                }]
            }]
        if reference or display:
            entry["individual"] = {"reference": reference}
            if display:
                entry["individual"]["display"] = display
        self.data["participant"].append(entry)
        return self

    def set_period(
        self,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> "EncounterBuilder":
        period: Dict[str, Any] = {}
        if start:
            period["start"] = start
        if end:
            period["end"] = end
        self.data["period"] = period
        return self

    def set_service_type(
        self,
        code: str,
        display: str,
        system: str = "http://terminology.hl7.org/CodeSystem/service-type",
    ) -> "EncounterBuilder":
        self.data["serviceType"] = {
            "coding": [{"system": system, "code": code, "display": display}]
        }
        return self

    def add_diagnosis(
        self,
        condition_ref: str,
        use_code: Optional[str] = None,
        use_display: Optional[str] = None,
        rank: Optional[int] = None,
    ) -> "EncounterBuilder":
        if "diagnosis" not in self.data:
            self.data["diagnosis"] = []
        diag: Dict[str, Any] = {"condition": {"reference": condition_ref}}
        if use_code:
            diag["use"] = {
                "coding": [{"code": use_code, "display": use_display}]
            }
        if rank:
            diag["rank"] = rank
        self.data["diagnosis"].append(diag)
        return self

    def set_hospitalization(
        self,
        admit_source_code: Optional[str] = None,
        admit_source_display: Optional[str] = None,
        discharge_disposition_code: Optional[str] = None,
        discharge_disposition_display: Optional[str] = None,
    ) -> "EncounterBuilder":
        hosp: Dict[str, Any] = {}
        if admit_source_code:
            hosp["admitSource"] = {
                "coding": [{"code": admit_source_code, "display": admit_source_display}]
            }
        if discharge_disposition_code:
            hosp["dischargeDisposition"] = {
                "coding": [{
                    "code": discharge_disposition_code,
                    "display": discharge_disposition_display,
                }]
            }
        self.data["hospitalization"] = hosp
        return self
