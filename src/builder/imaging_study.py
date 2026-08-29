"""ImagingStudy resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class ImagingStudyBuilder(BaseBuilder):
    """Builder for ImagingStudy resource."""

    def __init__(self):
        super().__init__("ImagingStudy")
    def set_id(self, id: str) -> "ImagingStudyBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "ImagingStudyBuilder":
        self.data["status"] = status
        return self

    def set_modality(self, code: str, system: str = "http://dicom.nema.org/resources/ontology/DCM", display: Optional[str] = None) -> "ImagingStudyBuilder":
        self.data.setdefault("modality", [])
        mod: dict = {"system": system, "code": code}
        if display:
            mod["display"] = display
        self.data["modality"].append(mod)
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "ImagingStudyBuilder":
        self.data["subject"] = {"reference": reference}
        if display:
            self.data["subject"]["display"] = display
        return self

    def set_encounter(self, reference: str) -> "ImagingStudyBuilder":
        self.data["encounter"] = {"reference": reference}
        return self

    def set_started(self, started: str) -> "ImagingStudyBuilder":
        self.data["started"] = started
        return self

    def set_description(self, description: str) -> "ImagingStudyBuilder":
        self.data["description"] = description
        return self

    def add_series(
        self,
        uid: str,
        modality_code: str,
        modality_system: str = "http://dicom.nema.org/resources/ontology/DCM",
        modality_display: Optional[str] = None,
        number: Optional[int] = None,
        description: Optional[str] = None
    ) -> "ImagingStudyBuilder":
        self.data.setdefault("series", [])
        series: dict = {
            "uid": uid,
            "modality": {"system": modality_system, "code": modality_code}
        }
        if modality_display:
            series["modality"]["display"] = modality_display
        if number is not None:
            series["number"] = number
        if description:
            series["description"] = description
        self.data["series"].append(series)
        return self

    def add_series_instance(
        self,
        series_index: int,
        uid: str,
        sop_class: str,
        sop_system: str = "urn:ietf:bcp:13"
    ) -> "ImagingStudyBuilder":
        if "series" in self.data and len(self.data["series"]) > series_index:
            self.data["series"][series_index].setdefault("instance", [])
            inst: dict = {"uid": uid, "sopClass": {"system": sop_system, "code": sop_class}}
            self.data["series"][series_index]["instance"].append(inst)
        return self

    def add_endpoint(self, reference: str, display: Optional[str] = None) -> "ImagingStudyBuilder":
        self.data.setdefault("endpoint", [])
        ep: dict = {"reference": reference}
        if display:
            ep["display"] = display
        self.data["endpoint"].append(ep)
        return self

    def add_procedure_reference(self, reference: str) -> "ImagingStudyBuilder":
        self.data.setdefault("procedureReference", [])
        self.data["procedureReference"].append({"reference": reference})
        return self

    def add_referencer(self, reference: str, display: Optional[str] = None) -> "ImagingStudyBuilder":
        self.data.setdefault("referrer", {"reference": reference})
        if display:
            self.data["referrer"]["display"] = display
        return self
