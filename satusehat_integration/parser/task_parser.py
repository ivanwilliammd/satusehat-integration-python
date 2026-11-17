"""TaskParser — parses FHIR Task resource."""
from __future__ import annotations

from typing import Any, Optional


def _remove_prefix(value: Optional[str], prefix: str) -> Optional[str]:
    if value and isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class TaskParser:
    def __init__(self, task: Optional[dict[str, Any]] = None) -> None:
        self.task: dict[str, Any] = task if isinstance(task, dict) else {}

    def get_identifiers(self) -> Any:
        return self.task.get("identifier")

    getIdentifiers = get_identifiers

    def get_instantiates_uri(self) -> Any:
        return self.task.get("instantiatesUri")

    getInstantiatesUri = get_instantiates_uri

    def get_status(self) -> Any:
        return self.task.get("status")

    getStatus = get_status

    def get_intent(self) -> Any:
        return self.task.get("intent")

    getIntent = get_intent

    def get_priority(self) -> Any:
        return self.task.get("priority")

    getPriority = get_priority

    def get_description(self) -> Any:
        return self.task.get("description")

    getDescription = get_description

    def get_for(self) -> Any:
        return self.task.get("for")

    getFor = get_for

    def get_for_reference(self) -> Optional[str]:
        for_obj = self.task.get("for")
        ref = for_obj.get("reference") if isinstance(for_obj, dict) else None
        return _remove_prefix(ref, "Patient/")

    getForReference = get_for_reference

    def get_encounter(self) -> Any:
        return self.task.get("encounter")

    getEncounter = get_encounter

    def get_encounter_reference(self) -> Optional[str]:
        enc = self.task.get("encounter")
        ref = enc.get("reference") if isinstance(enc, dict) else None
        return _remove_prefix(ref, "Encounter/")

    getEncounterReference = get_encounter_reference

    def get_authored_on(self) -> Any:
        return self.task.get("authoredOn")

    getAuthoredOn = get_authored_on

    def get_requester(self) -> Any:
        return self.task.get("requester")

    getRequester = get_requester

    def get_requester_reference(self) -> Optional[str]:
        req = self.task.get("requester")
        ref = req.get("reference") if isinstance(req, dict) else None
        return _remove_prefix(ref, "Practitioner/")

    getRequesterReference = get_requester_reference

    def get_inputs(self) -> Any:
        return self.task.get("input")

    getInputs = get_inputs
