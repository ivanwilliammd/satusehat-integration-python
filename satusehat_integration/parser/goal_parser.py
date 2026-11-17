"""GoalParser — typed accessors over the official SATUSEHAT Goal payload.

Shape source: satusehat-conformance/examples/satusehat/Goal.json, copied unchanged to
satusehat_integration/parser/testdata/Goal.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class GoalParser:
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

    def get_lifecycle_status(self) -> Any:
        return self.payload.get("lifecycleStatus")

    getLifecycleStatus = get_lifecycle_status

    def get_achievement_status(self) -> Any:
        return self.payload.get("achievementStatus")

    getAchievementStatus = get_achievement_status

    def get_category(self) -> Any:
        return self.payload.get("category")

    getCategory = get_category

    def get_description(self) -> Any:
        return self.payload.get("description")

    getDescription = get_description

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_target(self) -> Any:
        return self.payload.get("target")

    getTarget = get_target

    def get_status_date(self) -> Any:
        return self.payload.get("statusDate")

    getStatusDate = get_status_date

    def get_expressed_by(self) -> Any:
        return self.payload.get("expressedBy")

    getExpressedBy = get_expressed_by

    def get_addresses(self) -> Any:
        return self.payload.get("addresses")

    getAddresses = get_addresses

    def get_outcome_code(self) -> Any:
        return self.payload.get("outcomeCode")

    getOutcomeCode = get_outcome_code

    def get_priority(self) -> Any:
        return self._data.get("priority")

    getPriority = get_priority

    def get_start_date(self) -> Any:
        return self._data.get("startDate")

    getStartDate = get_start_date

    def get_start_codeable_concept(self) -> Any:
        return self._data.get("startCodeableConcept")

    getStartCodeableConcept = get_start_codeable_concept

    def get_status_reason(self) -> Any:
        return self._data.get("statusReason")

    getStatusReason = get_status_reason

    def get_note(self) -> Any:
        return self._data.get("note")

    getNote = get_note

    def get_outcome_reference(self) -> Any:
        return self._data.get("outcomeReference")

    getOutcomeReference = get_outcome_reference

    def get_subject_history(self) -> Any:
        return self._data.get("subjectHistory")

    getSubjectHistory = get_subject_history
