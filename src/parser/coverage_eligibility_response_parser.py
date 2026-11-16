"""CoverageEligibilityResponseParser — typed accessors over the official SATUSEHAT CoverageEligibilityResponse payload.

Shape source: satusehat-conformance/examples/satusehat/CoverageEligibilityResponse.json, copied unchanged to
src/parser/testdata/CoverageEligibilityResponse.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class CoverageEligibilityResponseParser:
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

    def get_purpose(self) -> Any:
        return self.payload.get("purpose")

    getPurpose = get_purpose

    def get_patient(self) -> Any:
        return self.payload.get("patient")

    getPatient = get_patient

    def get_created(self) -> Any:
        return self.payload.get("created")

    getCreated = get_created

    def get_requestor(self) -> Any:
        return self.payload.get("requestor")

    getRequestor = get_requestor

    def get_request(self) -> Any:
        return self.payload.get("request")

    getRequest = get_request

    def get_outcome(self) -> Any:
        return self.payload.get("outcome")

    getOutcome = get_outcome

    def get_disposition(self) -> Any:
        return self.payload.get("disposition")

    getDisposition = get_disposition

    def get_insurer(self) -> Any:
        return self.payload.get("insurer")

    getInsurer = get_insurer

    def get_insurance(self) -> Any:
        return self.payload.get("insurance")

    getInsurance = get_insurance

    def get_extension(self) -> Any:
        return self.payload.get("extension")

    getExtension = get_extension

    def get_serviced_date(self) -> Any:
        return self._data.get("servicedDate")

    getServicedDate = get_serviced_date

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_request_provider(self) -> Any:
        return self._data.get("requestProvider")

    getRequestProvider = get_request_provider

    def get_serviced_period(self) -> Any:
        return self._data.get("servicedPeriod")

    getServicedPeriod = get_serviced_period
