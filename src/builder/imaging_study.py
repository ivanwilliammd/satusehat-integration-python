"""ImagingStudy resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from .base import BaseBuilder


class ImagingStudyBuilder(BaseBuilder):
    """Builder for ImagingStudy resource."""

    def __init__(self):
        super().__init__()
        self._data = {"resourceType": "ImagingStudy"}

    def set_id(self, id: str) -> "ImagingStudyBuilder":
        self._data["id"] = id
        return self

    def set_status(self, status: str) -> "ImagingStudyBuilder":
        self._data["status"] = status
        return self

    def set_modality(self, code: str, system: str = "http://dicom.nema.org/resources/ontology/DCM", display: Optional[str] = None) -> "ImagingStudyBuilder":
        self._data.setdefault("modality", [])
        mod: dict = {"system": system, "code": code}
        if display:
            mod["display"] = display
        self._data["modality"].append(mod)
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "ImagingStudyBuilder":
        self._data["subject"] = {"reference": reference}
        if display:
            self._data["subject"]["display"] = display
        return self

    def set_encounter(self, reference: str) -> "ImagingStudyBuilder":
        self._data["encounter"] = {"reference": reference}
        return self

    def set_started(self, started: str) -> "ImagingStudyBuilder":
        self._data["started"] = started
        return self

    def set_description(self, description: str) -> "ImagingStudyBuilder":
        self._data["description"] = description
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
        self._data.setdefault("series", [])
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
        self._data["series"].append(series)
        return self

    def add_series_instance(
        self,
        series_index: int,
        uid: str,
        sop_class: str,
        sop_system: str = "urn:ietf:bcp:13"
    ) -> "ImagingStudyBuilder":
        if "series" in self._data and len(self._data["series"]) > series_index:
            self._data["series"][series_index].setdefault("instance", [])
            inst: dict = {"uid": uid, "sopClass": {"system": sop_system, "code": sop_class}}
            self._data["series"][series_index]["instance"].append(inst)
        return self

    def add_endpoint(self, reference: str, display: Optional[str] = None) -> "ImagingStudyBuilder":
        self._data.setdefault("endpoint", [])
        ep: dict = {"reference": reference}
        if display:
            ep["display"] = display
        self._data["endpoint"].append(ep)
        return self

    def add_procedure_reference(self, reference: str) -> "ImagingStudyBuilder":
        self._data.setdefault("procedureReference", [])
        self._data["procedureReference"].append({"reference": reference})
        return self

    def add_referencer(self, reference: str, display: Optional[str] = None) -> "ImagingStudyBuilder":
        self._data.setdefault("referrer", {"reference": reference})
        if display:
            self._data["referrer"]["display"] = display
        return self
