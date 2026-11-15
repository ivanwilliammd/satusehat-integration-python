"""Task resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderTask.php. Versi sebelumnya menulis dua elemen sebagai daftar
padahal R4 menuntut satu nilai:

- `add_reason_code` menumpuk ke `reasonCode`         (R4: 0..1 CodeableConcept)
- `add_reason_reference` menumpuk ke `reasonReference` (R4: 0..1 Reference)

Selain itu setter CodeableConcept menerima (code, display, system) sehingga bentuk
payload berbeda dari kanon yang menerima objek CodeableConcept. Keduanya dibetulkan;
nama lama dipertahankan sebagai alias ke bentuk kanon.

Quirk PHP ditiru dan ditandai: `add_restriction` selalu memberi awalan `Patient/`
pada requester, bahkan ketika pemanggil memberi id Practitioner.
"""
from typing import Any, Dict, Optional

from src.builder.base_builder import BaseBuilder


def _konsep(nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> Dict[str, Any]:
    """Terima objek CodeableConcept (dict) atau bentuk (system, code, display)."""
    if isinstance(nilai, dict):
        return nilai
    coding: Dict[str, Any] = {"system": nilai, "code": code or ""}
    if display:
        coding["display"] = display
    return {"coding": [coding]}


def _rujukan(nilai: Any, awalan: str, display: Optional[str] = None) -> Dict[str, Any]:
    """Terima objek Reference (dict) atau string; awalan resource ditambahkan bila perlu."""
    if isinstance(nilai, dict):
        return nilai
    ref = nilai
    if not ref.startswith(("urn:", "http://", "https://")) and "/" not in ref:
        ref = f"{awalan}/{ref}"
    hasil: Dict[str, Any] = {"reference": ref}
    if display is not None:
        hasil["display"] = display
    return hasil


class TaskBuilder(BaseBuilder):
    """Builder for Task resource."""

    VALID_STATUSES = [
        "draft", "requested", "received", "accepted", "rejected", "ready",
        "cancelled", "in-progress", "on-hold", "failed", "completed", "entered-in-error",
    ]
    VALID_INTENTS = [
        "unknown", "proposal", "plan", "order", "original-order",
        "reflex-order", "filler-order", "instance-order", "option",
    ]

    def __init__(self):
        super().__init__("Task")

    def _push(self, key: str, value: Any) -> "TaskBuilder":  # type: ignore[override]
        self.data.setdefault(key, []).append(value)
        return self

    def set_id(self, val: str) -> "TaskBuilder":
        self.data["id"] = val
        return self

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "TaskBuilder":
        if isinstance(identifier, dict):
            return self._push("identifier", identifier)
        return self._push("identifier", {"system": identifier, "value": value})

    def set_instantiates_canonical(self, val: str) -> "TaskBuilder":
        self.data["instantiatesCanonical"] = val
        return self

    def set_instantiates_uri(self, val: str) -> "TaskBuilder":
        self.data["instantiatesUri"] = val
        return self

    def set_status(self, val: str) -> "TaskBuilder":
        if val not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {val}")
        self.data["status"] = val
        return self

    def set_status_reason(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "TaskBuilder":
        self.data["statusReason"] = _konsep(nilai, code, display)
        return self

    def set_business_status(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "TaskBuilder":
        self.data["businessStatus"] = _konsep(nilai, code, display)
        return self

    def set_intent(self, val: str) -> "TaskBuilder":
        if val not in self.VALID_INTENTS:
            raise ValueError(f"Invalid intent: {val}")
        self.data["intent"] = val
        return self

    def set_priority(self, val: str) -> "TaskBuilder":
        self.data["priority"] = val
        return self

    def set_code(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "TaskBuilder":
        self.data["code"] = _konsep(nilai, code, display)
        return self

    def set_description(self, val: str) -> "TaskBuilder":
        self.data["description"] = val
        return self

    def set_focus(self, nilai: Any, display: Optional[str] = None) -> "TaskBuilder":
        self.data["focus"] = _rujukan(nilai, "QuestionnaireResponse", display)
        return self

    def set_for(self, nilai: Any, display: Optional[str] = None) -> "TaskBuilder":
        self.data["for"] = _rujukan(nilai, "Patient", display)
        return self

    def set_encounter(self, nilai: Any, display: Optional[str] = None) -> "TaskBuilder":
        self.data["encounter"] = _rujukan(nilai, "Encounter", display)
        return self

    def set_execution_period(self, period: Any, end: Optional[str] = None) -> "TaskBuilder":
        if isinstance(period, dict):
            self.data["executionPeriod"] = period
            return self
        hasil: Dict[str, Any] = {"start": period}
        if end:
            hasil["end"] = end
        self.data["executionPeriod"] = hasil
        return self

    def set_authored_on(self, dt: str) -> "TaskBuilder":
        self.data["authoredOn"] = dt
        return self

    def set_last_modified(self, dt: str) -> "TaskBuilder":
        self.data["lastModified"] = dt
        return self

    def set_requester(self, nilai: Any, display: Optional[str] = None) -> "TaskBuilder":
        self.data["requester"] = _rujukan(nilai, "Practitioner", display)
        return self

    def set_owner(self, nilai: Any, display: Optional[str] = None) -> "TaskBuilder":
        self.data["owner"] = _rujukan(nilai, "Practitioner", display)
        return self

    def set_location(self, nilai: Any, display: Optional[str] = None) -> "TaskBuilder":
        self.data["location"] = _rujukan(nilai, "Location", display)
        return self

    def set_reason_code(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "TaskBuilder":
        self.data["reasonCode"] = _konsep(nilai, code, display)
        return self

    def set_reason_reference(self, nilai: Any, display: Optional[str] = None) -> "TaskBuilder":
        self.data["reasonReference"] = _rujukan(nilai, "Condition", display)
        return self

    def add_input(self, tipe: Any, value: Any) -> "TaskBuilder":
        jenis = tipe if isinstance(tipe, dict) else {"text": tipe}
        return self._push("input", {"type": jenis, "valueString": str(value)})

    def add_output(self, tipe: Any, value: Any) -> "TaskBuilder":
        jenis = tipe if isinstance(tipe, dict) else {"text": tipe}
        return self._push("output", {"type": jenis, "valueString": str(value)})

    def add_restriction(self, requester: Any, repetitions: Optional[int] = None, period: Any = None) -> "TaskBuilder":
        """Quirk PHP: requester selalu diberi awalan `Patient/` bila tanpa garis miring."""
        if isinstance(requester, dict):
            ref = requester.get("reference", "")
        else:
            ref = requester
        if not ref.startswith(("urn:", "http://", "https://")) and "/" not in ref:
            ref = f"Patient/{ref}"
        restriction: Dict[str, Any] = {"requester": {"reference": ref}}
        if repetitions is not None:
            restriction["repetitions"] = repetitions
        if period is not None:
            restriction["period"] = period
        return self._push("restriction", restriction)

    def add_note(self, text: str) -> "TaskBuilder":
        return self._push("note", {"text": text})

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "TaskBuilder":
        extension: Dict[str, Any] = {"url": url}
        if value_type is not None:
            extension[f"value{value_type[0].upper()}{value_type[1:]}"] = value
        else:
            extension["valueString"] = value if isinstance(value, str) else value
        return self._push("extension", extension)

    # --- alias nama lama ------------------------------------------------------

    def add_reason_code(self, nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> "TaskBuilder":
        """Alias lama: menumpuk (salah menurut R4). Kini menimpa seperti kanon."""
        return self.set_reason_code(nilai, code, display)

    def add_reason_reference(self, nilai: Any, display: Optional[str] = None) -> "TaskBuilder":
        return self.set_reason_reference(nilai, display)
