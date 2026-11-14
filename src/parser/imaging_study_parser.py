"""ImagingStudyParser — typed accessors over the official SATUSEHAT ImagingStudy payload.

Shape source: satusehat-conformance/examples/satusehat/ImagingStudy.json, copied unchanged to
src/parser/testdata/ImagingStudy.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class ImagingStudyParser:
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

    def get_modality(self) -> Any:
        return self.payload.get("modality")

    getModality = get_modality

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_started(self) -> Any:
        return self.payload.get("started")

    getStarted = get_started

    def get_based_on(self) -> Any:
        return self.payload.get("basedOn")

    getBasedOn = get_based_on

    def get_number_of_series(self) -> Any:
        return self.payload.get("numberOfSeries")

    getNumberOfSeries = get_number_of_series

    def get_number_of_instances(self) -> Any:
        return self.payload.get("numberOfInstances")

    getNumberOfInstances = get_number_of_instances

    def get_description(self) -> Any:
        return self.payload.get("description")

    getDescription = get_description

    def get_series(self) -> Any:
        return self.payload.get("series")

    getSeries = get_series
