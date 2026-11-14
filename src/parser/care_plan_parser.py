"""CarePlanParser — typed accessors over the official SATUSEHAT CarePlan payload.

Shape source: satusehat-conformance/examples/satusehat/CarePlan.json, copied unchanged to
src/parser/testdata/CarePlan.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class CarePlanParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_title(self) -> Any:
        return self.payload.get("title")

    getTitle = get_title

    def get_description(self) -> Any:
        return self.payload.get("description")

    getDescription = get_description

    def get_category(self) -> Any:
        return self.payload.get("category")

    getCategory = get_category

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_intent(self) -> Any:
        return self.payload.get("intent")

    getIntent = get_intent

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_encounter(self) -> Any:
        return self.payload.get("encounter")

    getEncounter = get_encounter

    def get_period(self) -> Any:
        return self.payload.get("period")

    getPeriod = get_period

    def get_created(self) -> Any:
        return self.payload.get("created")

    getCreated = get_created

    def get_author(self) -> Any:
        return self.payload.get("author")

    getAuthor = get_author

    def get_activity(self) -> Any:
        return self.payload.get("activity")

    getActivity = get_activity
