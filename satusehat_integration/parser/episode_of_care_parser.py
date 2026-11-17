"""EpisodeOfCareParser — typed accessors over the official SATUSEHAT EpisodeOfCare payload.

Shape source: satusehat-conformance/examples/satusehat/EpisodeOfCare.json, copied unchanged to
satusehat_integration/parser/testdata/EpisodeOfCare.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class EpisodeOfCareParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_id(self) -> Any:
        return self.payload.get("id")

    getId = get_id

    def get_identifier(self) -> Any:
        return self.payload.get("identifier")

    getIdentifier = get_identifier

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_status_history(self) -> Any:
        return self.payload.get("statusHistory")

    getStatusHistory = get_status_history

    def get_type(self) -> Any:
        return self.payload.get("type")

    getType = get_type

    def get_diagnosis(self) -> Any:
        return self.payload.get("diagnosis")

    getDiagnosis = get_diagnosis

    def get_patient(self) -> Any:
        return self.payload.get("patient")

    getPatient = get_patient

    def get_managing_organization(self) -> Any:
        return self.payload.get("managingOrganization")

    getManagingOrganization = get_managing_organization

    def get_period(self) -> Any:
        return self.payload.get("period")

    getPeriod = get_period

    def get_care_manager(self) -> Any:
        return self.payload.get("careManager")

    getCareManager = get_care_manager
