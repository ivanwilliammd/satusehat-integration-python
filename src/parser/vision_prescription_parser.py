"""VisionPrescriptionParser — typed accessors over the official SATUSEHAT VisionPrescription payload.

Shape source: satusehat-conformance/examples/satusehat/VisionPrescription.json, copied unchanged to
src/parser/testdata/VisionPrescription.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class VisionPrescriptionParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_created(self) -> Any:
        return self.payload.get("created")

    getCreated = get_created

    def get_patient(self) -> Any:
        return self.payload.get("patient")

    getPatient = get_patient

    def get_encounter(self) -> Any:
        return self.payload.get("encounter")

    getEncounter = get_encounter

    def get_date_written(self) -> Any:
        return self.payload.get("dateWritten")

    getDateWritten = get_date_written

    def get_prescriber(self) -> Any:
        return self.payload.get("prescriber")

    getPrescriber = get_prescriber

    def get_lens_specification(self) -> Any:
        return self.payload.get("lensSpecification")

    getLensSpecification = get_lens_specification
