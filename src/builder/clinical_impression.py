"""ClinicalImpression resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderClinicalImpression.php. Versi sebelumnya sebelas method tanpa
awalan `set_`, dan `note` MENIMPA seluruh daftar catatan alih-alih menumpuk.

Ditambah: previousOpinion, investigation, finding (CodeableConcept dan Reference),
prognosisCodeableConcept, prognosisReference, supportingInfo.

Quirk kanon ditiru dan ditandai: `setPreviousOpinion` menulis `previousOpinion`,
padahal R4 ClinicalImpression memakai `previous`. `summary` tidak ada di kanon —
ditambahkan di sini sebagai satu-satunya setter yang sah R4 di luar kanon.
"""
from typing import Any, Dict, Optional

from src.builder.base_builder import BaseBuilder


def _konsep(nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> Dict[str, Any]:
    if isinstance(nilai, dict):
        return nilai
    coding: Dict[str, Any] = {"system": nilai, "code": code or ""}
    if display:
        coding["display"] = display
    return {"coding": [coding]}


def _rujukan(nilai: Any) -> Dict[str, Any]:
    return nilai if isinstance(nilai, dict) else {"reference": nilai}


class ClinicalImpressionBuilder(BaseBuilder):
    """Builder for ClinicalImpression resource."""

    def __init__(self) -> None:
        super().__init__("ClinicalImpression")

    def set_id(self, id: str) -> "ClinicalImpressionBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "ClinicalImpressionBuilder":
        if isinstance(identifier, dict):
            return self._push("identifier", identifier)
        return self._push("identifier", {"system": identifier, "value": value})

    def set_status(self, status: str) -> "ClinicalImpressionBuilder":
        self.data["status"] = status
        return self

    def set_code(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "ClinicalImpressionBuilder":
        self.data["code"] = _konsep(nilai, code, display)
        return self

    def set_subject(self, subject: Any, display: Optional[str] = None) -> "ClinicalImpressionBuilder":
        hasil = _rujukan(subject)
        if display:
            hasil["display"] = display
        self.data["subject"] = hasil
        return self

    def set_encounter(self, encounter: Any) -> "ClinicalImpressionBuilder":
        self.data["encounter"] = _rujukan(encounter)
        return self

    def set_effective_date_time(self, date_time: str) -> "ClinicalImpressionBuilder":
        self.data["effectiveDateTime"] = date_time
        return self

    def set_effective_period(self, period: Any) -> "ClinicalImpressionBuilder":
        self.data["effectivePeriod"] = period
        return self

    def set_date(self, date: str) -> "ClinicalImpressionBuilder":
        self.data["date"] = date
        return self

    def set_assessor(self, assessor: Any) -> "ClinicalImpressionBuilder":
        self.data["assessor"] = _rujukan(assessor)
        return self

    def set_previous_opinion(self, previous: Any) -> "ClinicalImpressionBuilder":
        """Quirk kanon: elemen R4-nya `previous`, bukan `previousOpinion`."""
        self.data["previousOpinion"] = _rujukan(previous)
        return self

    def add_investigation(self, investigation: Dict[str, Any]) -> "ClinicalImpressionBuilder":
        return self._push("investigation", investigation)

    def add_finding_codeable_concept(self, finding: Any) -> "ClinicalImpressionBuilder":
        return self._push("finding", {"itemCodeableConcept": _konsep(finding)})

    def add_finding_reference(self, finding: Any) -> "ClinicalImpressionBuilder":
        return self._push("finding", {"itemReference": _rujukan(finding)})

    def add_prognosis_codeable_concept(self, prognosis: Any) -> "ClinicalImpressionBuilder":
        return self._push("prognosisCodeableConcept", _konsep(prognosis))

    def add_prognosis_reference(self, prognosis: Any) -> "ClinicalImpressionBuilder":
        return self._push("prognosisReference", _rujukan(prognosis))

    def add_supporting_info(self, supporting_info: Any) -> "ClinicalImpressionBuilder":
        return self._push("supportingInfo", _rujukan(supporting_info))

    def add_note(self, note: Any) -> "ClinicalImpressionBuilder":
        return self._push("note", note if isinstance(note, dict) else {"text": note})

    # --- tambahan yang sah R4, tidak ada di kanon -----------------------------

    def set_summary(self, summary: str) -> "ClinicalImpressionBuilder":
        self.data["summary"] = summary
        return self

    # --- alias nama lama ------------------------------------------------------

    def identifier(self, identifier: Dict[str, Any]) -> "ClinicalImpressionBuilder":
        return self.add_identifier(identifier)

    def status(self, value: str) -> "ClinicalImpressionBuilder":
        return self.set_status(value)

    def code(self, konsep: Dict[str, Any]) -> "ClinicalImpressionBuilder":
        return self.set_code(konsep)

    def subject(self, reference: str, display: str = "") -> "ClinicalImpressionBuilder":
        return self.set_subject(reference, display or None)

    def encounter(self, reference: str) -> "ClinicalImpressionBuilder":
        return self.set_encounter(reference)

    def effective_date_time(self, value: str) -> "ClinicalImpressionBuilder":
        return self.set_effective_date_time(value)

    def effective_period(self, period: Dict[str, Any]) -> "ClinicalImpressionBuilder":
        return self.set_effective_period(period)

    def date(self, value: str) -> "ClinicalImpressionBuilder":
        return self.set_date(value)

    def assessor(self, reference: str) -> "ClinicalImpressionBuilder":
        return self.set_assessor(reference)

    def note(self, text: str) -> "ClinicalImpressionBuilder":
        """Alias lama: dulu MENIMPA daftar catatan; kini menumpuk seperti kanon."""
        return self.add_note(text)
