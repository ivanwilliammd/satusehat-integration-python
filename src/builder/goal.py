from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class GoalBuilder(BaseBuilder):
    _resourceType = "Goal"

    def __init__(self) -> None:
        super().__init__("GoalBuilder")

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
