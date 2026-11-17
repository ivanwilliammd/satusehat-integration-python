from typing import Any, List, Optional
from satusehat_integration.builder.base_builder import BaseBuilder


class GoalBuilder(BaseBuilder):
    _resourceType = "Goal"

    def __init__(self) -> None:
        super().__init__("Goal")

    def lifecycle_status(self, value: str) -> "GoalBuilder":
        return self._set("lifecycleStatus", value)

    def achievement_status(self, codeable_concept: dict) -> "GoalBuilder":
        return self._set("achievementStatus", codeable_concept)

    def category(self, codeable_concept: dict) -> "GoalBuilder":
        return self._append("category", codeable_concept)

    def priority(self, codeable_concept: dict) -> "GoalBuilder":
        return self._set("priority", codeable_concept)

    def description(self, codeable_concept: dict) -> "GoalBuilder":
        return self._set("description", codeable_concept)

    def subject(self, reference: str, display: Optional[str] = None) -> "GoalBuilder":
        sub: dict = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("subject", sub)

    def start_date(self, value: str) -> "GoalBuilder":
        return self._set("startDate", value)

    def start_codeable_concept(self, codeable_concept: dict) -> "GoalBuilder":
        return self._set("startCodeableConcept", codeable_concept)

    def target(self, measure_codeable_concept: dict, detail_quantity: Optional[dict] = None, detail_range: Optional[dict] = None, detail_codeable_concept: Optional[dict] = None, due_date: Optional[str] = None, due_period: Optional[dict] = None) -> "GoalBuilder":
        tgt: dict = {"measureCodeableConcept": measure_codeable_concept}
        if detail_quantity:
            tgt["detailQuantity"] = detail_quantity
        if detail_range:
            tgt["detailRange"] = detail_range
        if detail_codeable_concept:
            tgt["detailCodeableConcept"] = detail_codeable_concept
        if due_date:
            tgt["dueDate"] = due_date
        if due_period:
            tgt["duePeriod"] = due_period
        return self._append("target", tgt)

    def status_reason(self, text: str) -> "GoalBuilder":
        return self._set("statusReason", text)

    def note(self, text: str) -> "GoalBuilder":
        return self._append("note", {"text": text})

    def outcome_reference(self, reference: str, display: Optional[str] = None) -> "GoalBuilder":
        ref: dict = {"reference": reference}
        if display:
            ref["display"] = display
        return self._append("outcomeReference", ref)

    def outcome_code(self, codeable_concept: dict) -> "GoalBuilder":
        return self._append("outcomeCode", codeable_concept)

    def addresses(self, reference: str) -> "GoalBuilder":
        return self._append("addresses", {"reference": reference})

    def subject_history(self, reference: str) -> "GoalBuilder":
        return self._append("subjectHistory", {"reference": reference})

    # --- Nama kanon (cermin PayloadBuilderGoal) ---

    def set_id(self, id: str) -> "GoalBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "GoalBuilder":
        entry = {"system": identifier, "value": value} if value is not None else (
            identifier.to_array() if hasattr(identifier, "to_array") else identifier
        )
        self.data.setdefault("identifier", []).append(entry)
        return self

    def set_lifecycle_status(self, status: str) -> "GoalBuilder":
        self.data["lifecycleStatus"] = status
        return self

    def set_description(self, description: Any) -> "GoalBuilder":
        self.data["description"] = description.to_array() if hasattr(description, "to_array") else description
        return self

    def set_subject(self, subject: Any, display: Optional[str] = None) -> "GoalBuilder":
        if isinstance(subject, str):
            ref: Dict[str, Any] = {"reference": subject}
            if display:
                ref["display"] = display
            self.data["subject"] = ref
        else:
            self.data["subject"] = subject.to_array() if hasattr(subject, "to_array") else subject
        return self

    def set_start_date_time(self, start_date_time: str) -> "GoalBuilder":
        self.data["startDateTime"] = start_date_time
        return self

    def set_start_age(self, start_age: Any) -> "GoalBuilder":
        self.data["startAge"] = start_age.to_array() if hasattr(start_age, "to_array") else start_age
        return self

    def set_start_period(self, start_period: Any) -> "GoalBuilder":
        self.data["startPeriod"] = start_period.to_array() if hasattr(start_period, "to_array") else start_period
        return self

    def add_target_detail_quantity(self, detail: Any) -> "GoalBuilder":
        entry = detail.to_array() if hasattr(detail, "to_array") else detail
        self.data.setdefault("target", []).append({"detailQuantity": entry})
        return self

    def add_target_detail_codeable_concept(self, detail: Any) -> "GoalBuilder":
        entry = detail.to_array() if hasattr(detail, "to_array") else detail
        self.data.setdefault("target", []).append({"detailCodeableConcept": entry})
        return self

    def add_target_range(self, target_range: Any) -> "GoalBuilder":
        entry = target_range.to_array() if hasattr(target_range, "to_array") else target_range
        self.data.setdefault("target", []).append({"detailRange": entry})
        return self

    def set_status_reason(self, status_reason: str) -> "GoalBuilder":
        self.data["statusReason"] = status_reason
        return self

    def add_note(self, note: Any) -> "GoalBuilder":
        entry = {"text": note} if isinstance(note, str) else (
            note.to_array() if hasattr(note, "to_array") else note
        )
        self.data.setdefault("note", []).append(entry)
        return self

    def add_outcome_reference(self, outcome_reference: Any) -> "GoalBuilder":
        entry = {"reference": outcome_reference} if isinstance(outcome_reference, str) else (
            outcome_reference.to_array() if hasattr(outcome_reference, "to_array") else outcome_reference
        )
        self.data.setdefault("outcomeReference", []).append(entry)
        return self
