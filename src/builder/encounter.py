from typing import Any, Dict, List, Optional

from src.datatype.datatypes import Identifier
from src.builder.base_builder import BaseBuilder


class EncounterBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Encounter")

    def add_identifier(self, identifier: Identifier) -> "EncounterBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append(
            identifier.to_array() if hasattr(identifier, "to_array") else identifier
        )
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

    # --- Nama kanon (cermin PayloadBuilderEncounter) ---

    def set_id(self, id: str) -> "EncounterBuilder":
        self.data["id"] = id
        return self

    def add_type(self, encounter_type: Any) -> "EncounterBuilder":
        entry = encounter_type.to_array() if hasattr(encounter_type, "to_array") else encounter_type
        self.data.setdefault("type", []).append(entry)
        return self

    def add_location(self, location: Any, status: Optional[str] = None,
                     physical_type: Any = None, display: Optional[str] = None) -> "EncounterBuilder":
        if isinstance(location, str):
            loc: Dict[str, Any] = {"reference": location}
            if display:
                loc["display"] = display
        else:
            loc = location.to_array() if hasattr(location, "to_array") else location
        row: Dict[str, Any] = {"location": loc}
        if status is not None:
            row["status"] = status
        if physical_type is not None:
            row["physicalType"] = physical_type.to_array() if hasattr(physical_type, "to_array") else physical_type
        self.data.setdefault("location", []).append(row)
        return self

    def add_reason_code(self, reason_code: Any) -> "EncounterBuilder":
        entry = reason_code.to_array() if hasattr(reason_code, "to_array") else reason_code
        self.data.setdefault("reasonCode", []).append(entry)
        return self

    def add_reason_reference(self, reason_reference: Any) -> "EncounterBuilder":
        if isinstance(reason_reference, str):
            entry: Dict[str, Any] = {"reference": reason_reference}
        else:
            entry = reason_reference.to_array() if hasattr(reason_reference, "to_array") else reason_reference
        self.data.setdefault("reasonReference", []).append(entry)
        return self

    def add_diagnosis_canonical(self, condition: Any, rank: Optional[int] = None,
                                use: Any = None, role: Any = None) -> "EncounterBuilder":
        """Bentuk kanon: Reference + rank + use + role. Nama lama add_diagnosis tetap dipertahankan."""
        if isinstance(condition, str):
            cond: Dict[str, Any] = {"reference": condition}
        else:
            cond = condition.to_array() if hasattr(condition, "to_array") else condition
        diag: Dict[str, Any] = {"condition": cond}
        if rank is not None:
            diag["rank"] = rank
        if use is not None:
            diag["use"] = use.to_array() if hasattr(use, "to_array") else use
        if role is not None:
            diag["role"] = role.to_array() if hasattr(role, "to_array") else role
        self.data.setdefault("diagnosis", []).append(diag)
        return self

    def set_service_provider(self, service_provider: Any, display: Optional[str] = None) -> "EncounterBuilder":
        if isinstance(service_provider, str):
            ref: Dict[str, Any] = {"reference": service_provider}
            if display:
                ref["display"] = display
            self.data["serviceProvider"] = ref
        else:
            self.data["serviceProvider"] = (
                service_provider.to_array() if hasattr(service_provider, "to_array") else service_provider
            )
        return self

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "EncounterBuilder":
        extension: Dict[str, Any] = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        self.data.setdefault("extension", []).append(extension)
        return self
