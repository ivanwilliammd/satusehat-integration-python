"""ConditionParser — typed accessors over the official SATUSEHAT Condition payload.

Shape source: satusehat-conformance/examples/satusehat/Condition.json, copied unchanged to
src/parser/testdata/Condition.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class ConditionParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_clinical_status(self) -> Any:
        return self.payload.get("clinicalStatus")

    getClinicalStatus = get_clinical_status

    def get_verification_status(self) -> Any:
        return self.payload.get("verificationStatus")

    getVerificationStatus = get_verification_status

    def get_category(self) -> Any:
        return self.payload.get("category")

    getCategory = get_category

    def get_code(self) -> Any:
        return self.payload.get("code")

    getCode = get_code

    def get_stage(self) -> Any:
        return self.payload.get("stage")

    getStage = get_stage

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_encounter(self) -> Any:
        return self.payload.get("encounter")

    getEncounter = get_encounter

    def get_recorded_date(self) -> Any:
        return self.payload.get("recordedDate")

    getRecordedDate = get_recorded_date
