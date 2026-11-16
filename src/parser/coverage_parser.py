"""CoverageParser — typed accessors over the official SATUSEHAT Coverage payload.

Shape source: satusehat-conformance/examples/satusehat/Coverage.json, copied unchanged to
src/parser/testdata/Coverage.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class CoverageParser:
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

    def get_subscriber_id(self) -> Any:
        return self.payload.get("subscriberId")

    getSubscriberId = get_subscriber_id

    def get_beneficiary(self) -> Any:
        return self.payload.get("beneficiary")

    getBeneficiary = get_beneficiary

    def get_payor(self) -> Any:
        return self.payload.get("payor")

    getPayor = get_payor

    def get_class(self) -> Any:
        return self.payload.get("class")

    getClass = get_class

    def get_extension(self) -> Any:
        return self.payload.get("extension")

    getExtension = get_extension

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_policy_holder(self) -> Any:
        return self._data.get("policyHolder")

    getPolicyHolder = get_policy_holder

    def get_subscriber(self) -> Any:
        return self._data.get("subscriber")

    getSubscriber = get_subscriber

    def get_dependent(self) -> Any:
        return self._data.get("dependent")

    getDependent = get_dependent

    def get_relationship(self) -> Any:
        return self._data.get("relationship")

    getRelationship = get_relationship

    def get_order(self) -> Any:
        return self._data.get("order")

    getOrder = get_order

    def get_network(self) -> Any:
        return self._data.get("network")

    getNetwork = get_network

    def get_period(self) -> Any:
        return self._data.get("period")

    getPeriod = get_period
