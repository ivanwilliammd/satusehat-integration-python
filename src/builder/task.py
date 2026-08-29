"""Task resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class TaskBuilder(BaseBuilder):
    """Builder for Task resource."""

    def __init__(self):
        super().__init__("TaskBuilder")
        self.data = {"resourceType": "Task"}

    def set_id(self, id: str) -> "TaskBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "TaskBuilder":
        self.data["status"] = status
        return self

    def set_intent(self, intent: str) -> "TaskBuilder":
        self.data["intent"] = intent
        return self

    def set_priority(self, priority: str) -> "TaskBuilder":
        self.data["priority"] = priority
        return self

    def set_code(self, code: str, system: str, display: Optional[str] = None) -> "TaskBuilder":
        self.data["code"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["code"]["coding"][0]["display"] = display
        return self

    def set_description(self, description: str) -> "TaskBuilder":
        self.data["description"] = description
        return self

    def set_focus(self, reference: str, display: Optional[str] = None) -> "TaskBuilder":
        self.data["focus"] = {"reference": reference}
        if display:
            self.data["focus"]["display"] = display
        return self

    def set_for(self, reference: str, display: Optional[str] = None) -> "TaskBuilder":
        self.data["for"] = {"reference": reference}
        if display:
            self.data["for"]["display"] = display
        return self

    def set_encounter(self, reference: str) -> "TaskBuilder":
        self.data["encounter"] = {"reference": reference}
        return self

    def set_execution_period(self, start: Optional[str] = None, end: Optional[str] = None) -> "TaskBuilder":
        period: dict = {}
        if start:
            period["start"] = start
        if end:
            period["end"] = end
        self.data["executionPeriod"] = period
        return self

    def set_restriction(
        self,
        repetitions: Optional[int] = None,
        period_start: Optional[str] = None,
        period_end: Optional[str] = None
    ) -> "TaskBuilder":
        restriction: dict = {}
        if repetitions:
            restriction["repeat"] = {"count": repetitions}
        if period_start or period_end:
            restriction["period"] = {}
            if period_start:
                restriction["period"]["start"] = period_start
            if period_end:
                restriction["period"]["end"] = period_end
        self.data["restriction"] = restriction
        return self

    def set_owner(self, reference: str, display: Optional[str] = None) -> "TaskBuilder":
        self.data["owner"] = {"reference": reference}
        if display:
            self.data["owner"]["display"] = display
        return self

    def set_authored_on(self, authored_on: str) -> "TaskBuilder":
        self.data["authoredOn"] = authored_on
        return self

    def set_last_modified(self, last_modified: str) -> "TaskBuilder":
        self.data["lastModified"] = last_modified
        return self

    def add_input(self, name: str, value: str, type_code: str, type_system: str) -> "TaskBuilder":
        self.data.setdefault("input", [])
        inp: dict = {
            "type": {"coding": [{"code": type_code, "system": type_system}]},
            "valueString": value
        }
        self.data["input"].append(inp)
        return self

    def add_output(self, name: str, value: str, type_code: str, type_system: str) -> "TaskBuilder":
        self.data.setdefault("output", [])
        out: dict = {
            "type": {"coding": [{"code": type_code, "system": type_system}]},
            "valueString": value
        }
        self.data["output"].append(out)
        return self

    def add_note(self, text: str) -> "TaskBuilder":
        self.data.setdefault("note", [])
        self.data["note"].append({"text": text})
        return self
