"""Task resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class TaskBuilder(BaseBuilder):
    """Builder for Task resource."""

    VALID_STATUSES = [
        'draft', 'requested', 'received', 'accepted', 'rejected', 'ready',
        'cancelled', 'in-progress', 'on-hold', 'failed', 'completed', 'entered-in-error',
    ]
    VALID_INTENTS = [
        'unknown', 'proposal', 'plan', 'order', 'original-order',
        'reflex-order', 'filler-order', 'instance-order', 'option',
    ]

    def __init__(self):
        super().__init__("Task")

    def set_id(self, val: str) -> "TaskBuilder":
        self.data["id"] = val
        return self

    def add_identifier(self, system: str, value: str) -> "TaskBuilder":
        self._push("identifier", {"system": system, "value": value})
        return self

    def set_instantiates_canonical(self, val: str) -> "TaskBuilder":
        self.data["instantiatesCanonical"] = val
        return self

    def set_instantiates_uri(self, val: str) -> "TaskBuilder":
        self.data["instantiatesUri"] = val
        return self

    def set_status(self, val: str) -> "TaskBuilder":
        if val not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {val}")
        self.data["status"] = val
        return self

    def set_status_reason(self, code: str, display: str = None, system: str = None) -> "TaskBuilder":
        coding = {"code": code, "display": display if display else code}
        if system:
            coding["system"] = system
        self.data["statusReason"] = {"coding": [coding]}
        return self

    def set_business_status(self, code: str, display: str = None, system: str = None) -> "TaskBuilder":
        coding = {"code": code, "display": display if display else code}
        if system:
            coding["system"] = system
        self.data["businessStatus"] = {"coding": [coding]}
        return self

    def set_intent(self, val: str) -> "TaskBuilder":
        if val not in self.VALID_INTENTS:
            raise ValueError(f"Invalid intent: {val}")
        self.data["intent"] = val
        return self

    def set_priority(self, val: str) -> "TaskBuilder":
        self.data["priority"] = val
        return self

    def set_code(self, code: str, display: str = None, system: str = None) -> "TaskBuilder":
        coding = {"code": code, "display": display if display else code}
        if system:
            coding["system"] = system
        self.data["code"] = {"coding": [coding]}
        return self

    def set_description(self, val: str) -> "TaskBuilder":
        self.data["description"] = val
        return self

    def set_focus(self, ref: str, display: str = None) -> "TaskBuilder":
        self.data["focus"] = self._ref(ref, "QuestionnaireResponse", display)
        return self

    def set_for(self, ref: str, display: str = None) -> "TaskBuilder":
        self.data["for"] = self._ref(ref, "Patient", display)
        return self

    def set_encounter(self, ref: str, display: str = None) -> "TaskBuilder":
        self.data["encounter"] = self._ref(ref, "Encounter", display)
        return self

    def set_execution_period(self, start: str, end: str = None) -> "TaskBuilder":
        period: dict = {"start": start}
        if end:
            period["end"] = end
        self.data["executionPeriod"] = period
        return self

    def set_authored_on(self, dt: str) -> "TaskBuilder":
        self.data["authoredOn"] = dt
        return self

    def set_last_modified(self, dt: str) -> "TaskBuilder":
        self.data["lastModified"] = dt
        return self

    def set_requester(self, ref: str, display: str = None) -> "TaskBuilder":
        self.data["requester"] = self._ref(ref, "Practitioner", display)
        return self

    def set_owner(self, ref: str, display: str = None) -> "TaskBuilder":
        self.data["owner"] = self._ref(ref, "Practitioner", display)
        return self

    def set_location(self, ref: str, display: str = None) -> "TaskBuilder":
        self.data["location"] = self._ref(ref, "Location", display)
        return self

    def add_reason_code(self, cc: dict) -> "TaskBuilder":
        self._push("reasonCode", cc)
        return self

    def add_reason_reference(self, ref: str) -> "TaskBuilder":
        self._push("reasonReference", {"reference": ref})
        return self

    def add_input(self, type_text: str, value: str) -> "TaskBuilder":
        self._push("input", {"type": {"text": type_text}, "valueString": value})
        return self

    def add_output(self, type_text: str, value: str) -> "TaskBuilder":
        self._push("output", {"type": {"text": type_text}, "valueString": value})
        return self

    def add_restriction(self, ref: str, repetitions: int = None) -> "TaskBuilder":
        restriction: dict = {"requester": {"reference": self._auto_prefix(ref, "Patient")}}
        if repetitions is not None:
            restriction["repetitions"] = repetitions
        self._push("restriction", restriction)
        return self

    def add_note(self, text: str) -> "TaskBuilder":
        self._push("note", {"text": text})
        return self

    def add_extension(self, url: str, value: str) -> "TaskBuilder":
        self._push("extension", {"url": url, "valueString": value})
        return self
