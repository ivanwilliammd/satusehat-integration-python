"""MolecularSequenceParser — parses FHIR MolecularSequence resource."""
from __future__ import annotations

from typing import Any, Optional


def _remove_prefix(value: Optional[str], prefix: str) -> Optional[str]:
    if value and isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class MolecularSequenceParser:
    def __init__(self, molecular_sequence: Optional[dict[str, Any]] = None) -> None:
        self.molecular_sequence: dict[str, Any] = (
            molecular_sequence if isinstance(molecular_sequence, dict) else {}
        )

    def get_text(self) -> Any:
        return self.molecular_sequence.get("text")

    getText = get_text

    def get_type(self) -> Any:
        return self.molecular_sequence.get("type")

    getType = get_type

    def get_coordinate_system(self) -> Any:
        return self.molecular_sequence.get("coordinateSystem")

    getCoordinateSystem = get_coordinate_system

    def get_patient_reference(self) -> Optional[str]:
        pat = self.molecular_sequence.get("patient")
        ref = pat.get("reference") if isinstance(pat, dict) else None
        return _remove_prefix(ref, "Patient/")

    getPatientReference = get_patient_reference

    def get_specimen_reference(self) -> Optional[str]:
        spec = self.molecular_sequence.get("specimen")
        ref = spec.get("reference") if isinstance(spec, dict) else None
        return _remove_prefix(ref, "Specimen/")

    getSpecimenReference = get_specimen_reference

    def get_device_reference(self) -> Optional[str]:
        dev = self.molecular_sequence.get("device")
        ref = dev.get("reference") if isinstance(dev, dict) else None
        return _remove_prefix(ref, "Device/")

    getDeviceReference = get_device_reference

    def get_performer_reference(self) -> Optional[str]:
        perf = self.molecular_sequence.get("performer")
        ref = perf.get("reference") if isinstance(perf, dict) else None
        return _remove_prefix(ref, "Organization/")

    getPerformerReference = get_performer_reference

    def get_reference_seq(self) -> Any:
        return self.molecular_sequence.get("referenceSeq")

    getReferenceSeq = get_reference_seq

    def get_variants(self) -> Any:
        return self.molecular_sequence.get("variant")

    getVariants = get_variants
