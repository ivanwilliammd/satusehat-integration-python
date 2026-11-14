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
