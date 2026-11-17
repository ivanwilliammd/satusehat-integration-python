"""ClaimParser — typed accessors over the official SATUSEHAT Claim payload.

Shape source: satusehat-conformance/examples/satusehat/Claim.json, copied unchanged to
satusehat_integration/parser/testdata/Claim.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class ClaimParser:
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

    def get_type(self) -> Any:
        return self.payload.get("type")

    getType = get_type

    def get_use(self) -> Any:
        return self.payload.get("use")

    getUse = get_use

    def get_patient(self) -> Any:
        return self.payload.get("patient")

    getPatient = get_patient

    def get_billable_period(self) -> Any:
        return self.payload.get("billablePeriod")

    getBillablePeriod = get_billable_period

    def get_created(self) -> Any:
        return self.payload.get("created")

    getCreated = get_created

    def get_enterer(self) -> Any:
        return self.payload.get("enterer")

    getEnterer = get_enterer

    def get_insurer(self) -> Any:
        return self.payload.get("insurer")

    getInsurer = get_insurer

    def get_provider(self) -> Any:
        return self.payload.get("provider")

    getProvider = get_provider

    def get_priority(self) -> Any:
        return self.payload.get("priority")

    getPriority = get_priority

    def get_payee(self) -> Any:
        return self.payload.get("payee")

    getPayee = get_payee

    def get_facility(self) -> Any:
        return self.payload.get("facility")

    getFacility = get_facility

    def get_supporting_info(self) -> Any:
        return self.payload.get("supportingInfo")

    getSupportingInfo = get_supporting_info

    def get_diagnosis(self) -> Any:
        return self.payload.get("diagnosis")

    getDiagnosis = get_diagnosis

    def get_procedure(self) -> Any:
        return self.payload.get("procedure")

    getProcedure = get_procedure

    def get_insurance(self) -> Any:
        return self.payload.get("insurance")

    getInsurance = get_insurance

    def get_total(self) -> Any:
        return self.payload.get("total")

    getTotal = get_total

    def get_extension(self) -> Any:
        return self.payload.get("extension")

    getExtension = get_extension
