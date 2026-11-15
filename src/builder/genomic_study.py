"""GenomicStudy builder.

PERHATIAN: `GenomicStudy` tidak ada di FHIR R4 inti (R4 punya `MolecularSequence` dan
`Observation`; `GenomicStudy` baru muncul di R5). Payload-nya hanya berguna bila
server memang mengenal resource ini.

Setara PayloadBuilderGenomicStudy.php. Versi sebelumnya hanya enam method tanpa
awalan `set_`, dengan dua cacat yang sama seperti versi Node:

- `started` menulis elemen `started`, padahal kanon menulis `startDate` — nama yang
  salah berarti nilainya tidak pernah terbaca;
- `type` menimpa, padahal kanon menumpuk (0..*);
- `set_status` tidak memvalidasi lima nilai yang sah.
"""
from typing import Any, Dict, Optional

from src.builder.base_builder import BaseBuilder

PARTICIPATION = "http://terminology.hl7.org/3.1.0/CodeSystem-v3-ParticipationType.html"


def _konsep(nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> Dict[str, Any]:
    if isinstance(nilai, dict):
        return nilai
    coding: Dict[str, Any] = {"system": nilai, "code": code or ""}
    if display:
        coding["display"] = display
    return {"coding": [coding]}


class GenomicStudyBuilder(BaseBuilder):
    """Builder untuk resource GenomicStudy (bukan R4 inti)."""

    VALID_STATUSES = ["registered", "available", "cancelled", "entered-in-error", "unknown"]

    def __init__(self) -> None:
        super().__init__("GenomicStudy")

    def set_meta_profile(self, profile: str) -> "GenomicStudyBuilder":
        return self._push("meta/profile", profile)

    def set_id(self, id: str) -> "GenomicStudyBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "GenomicStudyBuilder":
        if isinstance(identifier, dict):
            return self._push("identifier", identifier)
        return self._push("identifier", {"system": identifier, "value": value})

    def set_status(self, status: str) -> "GenomicStudyBuilder":
        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{status}'. Valid values: " + ", ".join(self.VALID_STATUSES)
            )
        self.data["status"] = status
        return self

    def add_type(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "GenomicStudyBuilder":
        return self._push("type", _konsep(nilai, code, display))

    def set_subject(self, reference: Any) -> "GenomicStudyBuilder":
        self.data["subject"] = reference if isinstance(reference, dict) else {"reference": reference}
        return self

    def set_encounter(self, reference: Any) -> "GenomicStudyBuilder":
        self.data["encounter"] = reference if isinstance(reference, dict) else {"reference": reference}
        return self

    def set_start_date(self, start_date: str) -> "GenomicStudyBuilder":
        self.data["startDate"] = start_date
        return self

    def add_based_on(self, reference: Any) -> "GenomicStudyBuilder":
        return self._push("basedOn", reference if isinstance(reference, dict) else {"reference": reference})

    def set_referrer(self, reference: Any) -> "GenomicStudyBuilder":
        self.data["referrer"] = reference if isinstance(reference, dict) else {"reference": reference}
        return self

    def add_interpreter(self, reference: Any) -> "GenomicStudyBuilder":
        return self._push("interpreter", reference if isinstance(reference, dict) else {"reference": reference})

    def add_reason(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "GenomicStudyBuilder":
        return self._push("reason", {"concept": _konsep(nilai, code, display)})

    def add_note(self, note: Any) -> "GenomicStudyBuilder":
        return self._push("note", note if isinstance(note, dict) else {"text": note})

    def set_description(self, description: str) -> "GenomicStudyBuilder":
        self.data["description"] = description
        return self

    def add_analysis(self, analysis: Dict[str, Any]) -> "GenomicStudyBuilder":
        return self._push("analysis", analysis)

    def add_performer(self, actor: Any, role: str = "PERF") -> "GenomicStudyBuilder":
        return self._push(
            "performer",
            {
                "actor": actor if isinstance(actor, dict) else {"reference": actor},
                "role": {"coding": [{"system": PARTICIPATION, "code": role, "display": "Performer"}]},
            },
        )

    # --- alias nama lama ------------------------------------------------------

    def status(self, value: str) -> "GenomicStudyBuilder":
        return self.set_status(value)

    def type(self, konsep: Dict[str, Any]) -> "GenomicStudyBuilder":
        """Alias lama: dulu menimpa; kini menumpuk seperti kanon."""
        return self.add_type(konsep)

    def subject(self, reference: str) -> "GenomicStudyBuilder":
        return self.set_subject(reference)

    def encounter(self, reference: str) -> "GenomicStudyBuilder":
        return self.set_encounter(reference)

    def started(self, value: str) -> "GenomicStudyBuilder":
        """Alias lama: dulu menulis `started`; kini menulis `startDate` seperti kanon."""
        return self.set_start_date(value)

    def based_on(self, reference: str) -> "GenomicStudyBuilder":
        return self.add_based_on(reference)
