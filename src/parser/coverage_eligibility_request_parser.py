"""CoverageEligibilityRequestParser — typed accessors over the official SATUSEHAT CoverageEligibilityRequest payload.

Shape source: satusehat-conformance/examples/satusehat/CoverageEligibilityRequest.json, copied unchanged to
src/parser/testdata/CoverageEligibilityRequest.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class CoverageEligibilityRequestParser:
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

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_priority(self) -> Any:
        return self.payload.get("priority")

    getPriority = get_priority

    def get_purpose(self) -> Any:
        return self.payload.get("purpose")

    getPurpose = get_purpose

    def get_patient(self) -> Any:
        return self.payload.get("patient")

    getPatient = get_patient

    def get_serviced_date(self) -> Any:
        return self.payload.get("servicedDate")

    getServicedDate = get_serviced_date

    def get_created(self) -> Any:
        return self.payload.get("created")

    getCreated = get_created

    def get_enterer(self) -> Any:
        return self.payload.get("enterer")

    getEnterer = get_enterer

    def get_provider(self) -> Any:
        return self.payload.get("provider")

    getProvider = get_provider

    def get_insurer(self) -> Any:
        return self.payload.get("insurer")

    getInsurer = get_insurer

    def get_facility(self) -> Any:
        return self.payload.get("facility")

    getFacility = get_facility

    def get_insurance(self) -> Any:
        return self.payload.get("insurance")

    getInsurance = get_insurance

    def get_supporting_info(self) -> Any:
        return self.payload.get("supportingInfo")

    getSupportingInfo = get_supporting_info

    def get_contained(self) -> Any:
        return self.payload.get("contained")

    getContained = get_contained

    def get_requestor(self) -> Any:
        return self._data.get("requestor")

    getRequestor = get_requestor

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_serviced_period(self) -> Any:
        return self._data.get("servicedPeriod")

    getServicedPeriod = get_serviced_period
