"""AllergyIntoleranceParser — typed accessors over the official SATUSEHAT AllergyIntolerance payload.

Shape source: satusehat-conformance/examples/satusehat/AllergyIntolerance.json, copied unchanged to
src/parser/testdata/AllergyIntolerance.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class AllergyIntoleranceParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_identifier(self) -> Any:
        return self.payload.get("identifier")

    getIdentifier = get_identifier

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

    def get_patient(self) -> Any:
        return self.payload.get("patient")

    getPatient = get_patient

    def get_encounter(self) -> Any:
        return self.payload.get("encounter")

    getEncounter = get_encounter

    def get_recorded_date(self) -> Any:
        return self.payload.get("recordedDate")

    getRecordedDate = get_recorded_date

    def get_recorder(self) -> Any:
        return self.payload.get("recorder")

    getRecorder = get_recorder

    def get_type(self) -> Any:
        return self._data.get("type")

    getType = get_type

    def get_onset_date_time(self) -> Any:
        return self._data.get("onsetDateTime")

    getOnsetDateTime = get_onset_date_time

    def get_asserter(self) -> Any:
        return self._data.get("asserter")

    getAsserter = get_asserter

    def get_note(self) -> Any:
        return self._data.get("note")

    getNote = get_note
