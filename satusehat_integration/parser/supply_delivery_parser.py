"""SupplyDeliveryParser — typed accessors over the official SATUSEHAT SupplyDelivery payload.

Shape source: satusehat-conformance/examples/satusehat/SupplyDelivery.json, copied unchanged to
satusehat_integration/parser/testdata/SupplyDelivery.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class SupplyDeliveryParser:
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

    def get_based_on(self) -> Any:
        return self.payload.get("basedOn")

    getBasedOn = get_based_on

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_patient(self) -> Any:
        return self.payload.get("patient")

    getPatient = get_patient

    def get_supplied_item(self) -> Any:
        return self.payload.get("suppliedItem")

    getSuppliedItem = get_supplied_item

    def get_occurrence_date_time(self) -> Any:
        return self.payload.get("occurrenceDateTime")

    getOccurrenceDateTime = get_occurrence_date_time

    def get_supplier(self) -> Any:
        return self.payload.get("supplier")

    getSupplier = get_supplier

    def get_destination(self) -> Any:
        return self.payload.get("destination")

    getDestination = get_destination

    def get_receiver(self) -> Any:
        return self.payload.get("receiver")

    getReceiver = get_receiver

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_code(self) -> Any:
        return self._data.get("code")

    getCode = get_code

    def get_subject(self) -> Any:
        return self._data.get("subject")

    getSubject = get_subject

    def get_description(self) -> Any:
        return self._data.get("description")

    getDescription = get_description

    def get_encounter(self) -> Any:
        return self._data.get("encounter")

    getEncounter = get_encounter
