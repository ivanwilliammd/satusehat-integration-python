"""FamilyMemberHistoryParser — typed accessors over the official SATUSEHAT FamilyMemberHistory payload.

Shape source: satusehat-conformance/examples/satusehat/FamilyMemberHistory.json, copied unchanged to
src/parser/testdata/FamilyMemberHistory.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class FamilyMemberHistoryParser:
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

    def get_relationship(self) -> Any:
        return self.payload.get("relationship")

    getRelationship = get_relationship

    def get_deceased_boolean(self) -> Any:
        return self.payload.get("deceasedBoolean")

    getDeceasedBoolean = get_deceased_boolean

    def get_patient(self) -> Any:
        return self.payload.get("patient")

    getPatient = get_patient

    def get_date(self) -> Any:
        return self.payload.get("date")

    getDate = get_date

    def get_condition(self) -> Any:
        return self.payload.get("condition")

    getCondition = get_condition

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_instantiates_canonical(self) -> Any:
        return self._data.get("instantiatesCanonical")

    getInstantiatesCanonical = get_instantiates_canonical

    def get_data_absent_reason(self) -> Any:
        return self._data.get("dataAbsentReason")

    getDataAbsentReason = get_data_absent_reason

    def get_name(self) -> Any:
        return self._data.get("name")

    getName = get_name

    def get_sex(self) -> Any:
        return self._data.get("sex")

    getSex = get_sex

    def get_born_period(self) -> Any:
        return self._data.get("bornPeriod")

    getBornPeriod = get_born_period

    def get_born_date(self) -> Any:
        return self._data.get("bornDate")

    getBornDate = get_born_date

    def get_born_string(self) -> Any:
        return self._data.get("bornString")

    getBornString = get_born_string

    def get_age_age(self) -> Any:
        return self._data.get("ageAge")

    getAgeAge = get_age_age

    def get_age_unit(self) -> Any:
        return self._data.get("ageUnit")

    getAgeUnit = get_age_unit

    def get_age_range(self) -> Any:
        return self._data.get("ageRange")

    getAgeRange = get_age_range

    def get_age_string(self) -> Any:
        return self._data.get("ageString")

    getAgeString = get_age_string

    def get_deceased_age(self) -> Any:
        return self._data.get("deceasedAge")

    getDeceasedAge = get_deceased_age

    def get_deceased_age_unit(self) -> Any:
        return self._data.get("deceasedAgeUnit")

    getDeceasedAgeUnit = get_deceased_age_unit

    def get_deceased_range(self) -> Any:
        return self._data.get("deceasedRange")

    getDeceasedRange = get_deceased_range

    def get_deceased_date(self) -> Any:
        return self._data.get("deceasedDate")

    getDeceasedDate = get_deceased_date

    def get_deceased_string(self) -> Any:
        return self._data.get("deceasedString")

    getDeceasedString = get_deceased_string

    def get_deceased_codeable_concept(self) -> Any:
        return self._data.get("deceasedCodeableConcept")

    getDeceasedCodeableConcept = get_deceased_codeable_concept

    def get_reason_code(self) -> Any:
        return self._data.get("reasonCode")

    getReasonCode = get_reason_code

    def get_code(self) -> Any:
        return self._data.get("code")

    getCode = get_code
