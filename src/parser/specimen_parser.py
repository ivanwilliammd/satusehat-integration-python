"""SpecimenParser — parses FHIR Specimen resource."""
from __future__ import annotations

from typing import Any, Optional


def _remove_prefix(value: Optional[str], prefix: str) -> Optional[str]:
    if value and isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class SpecimenParser:
    def __init__(self, specimen: Optional[dict[str, Any]] = None) -> None:
        self.specimen: dict[str, Any] = specimen if isinstance(specimen, dict) else {}

    def get_identifiers(self) -> Any:
        return self.specimen.get("identifier")

    getIdentifiers = get_identifiers

    def get_status(self) -> Any:
        return self.specimen.get("status")

    getStatus = get_status

    def get_type(self) -> Any:
        return self.specimen.get("type")

    getType = get_type

    def get_subject(self) -> Any:
        return self.specimen.get("subject")

    getSubject = get_subject

    def get_subject_reference(self) -> Optional[str]:
        subj = self.specimen.get("subject")
        ref = subj.get("reference") if isinstance(subj, dict) else None
        return _remove_prefix(ref, "Patient/")

    getSubjectReference = get_subject_reference

    def get_subject_display(self) -> Optional[str]:
        subj = self.specimen.get("subject")
        return subj.get("display") if isinstance(subj, dict) else None

    getSubjectDisplay = get_subject_display

    def get_received_time(self) -> Any:
        return self.specimen.get("receivedTime")

    getReceivedTime = get_received_time

    def get_requests(self) -> Any:
        return self.specimen.get("request")

    getRequests = get_requests

    def get_collected_date_time(self) -> Any:
        coll = self.specimen.get("collection")
        return coll.get("collectedDateTime") if isinstance(coll, dict) else None

    getCollectedDateTime = get_collected_date_time

    def get_collector(self) -> Any:
        coll = self.specimen.get("collection")
        return coll.get("collector") if isinstance(coll, dict) else None

    getCollector = get_collector

    def get_collector_reference(self) -> Optional[str]:
        coll = self.specimen.get("collection")
        collector = coll.get("collector") if isinstance(coll, dict) else None
        ref = collector.get("reference") if isinstance(collector, dict) else None
        return _remove_prefix(ref, "Practitioner/")

    getCollectorReference = get_collector_reference

    def get_collector_display(self) -> Optional[str]:
        coll = self.specimen.get("collection")
        collector = coll.get("collector") if isinstance(coll, dict) else None
        return collector.get("display") if isinstance(collector, dict) else None

    getCollectorDisplay = get_collector_display

    def get_fasting_status(self) -> Any:
        coll = self.specimen.get("collection")
        return coll.get("fastingStatusCodeableConcept") if isinstance(coll, dict) else None

    getFastingStatus = get_fasting_status

    def get_method(self) -> Any:
        coll = self.specimen.get("collection")
        return coll.get("method") if isinstance(coll, dict) else None

    getMethod = get_method

    def get_quantity(self) -> Any:
        coll = self.specimen.get("collection")
        return coll.get("quantity") if isinstance(coll, dict) else None

    getQuantity = get_quantity

    def get_body_site(self) -> Any:
        coll = self.specimen.get("collection")
        return coll.get("bodySite") if isinstance(coll, dict) else None

    getBodySite = get_body_site

    def get_conditions(self) -> Any:
        return self.specimen.get("condition")

    getConditions = get_conditions

    def get_extensions(self) -> Any:
        return self.specimen.get("extension")

    getExtensions = get_extensions

    def get_processing(self) -> Any:
        return self.specimen.get("processing")

    getProcessing = get_processing
