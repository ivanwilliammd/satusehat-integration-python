from src.builder.base_builder import BaseBuilder


class SupplyRequestBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("SupplyRequest")

    def set_status(self, status: str) -> "SupplyRequestBuilder":
        self.data["status"] = status
        return self

    def set_priority(self, priority: str) -> "SupplyRequestBuilder":
        self.data["priority"] = priority
        return self

    def set_subject(self, subject_ref: str) -> "SupplyRequestBuilder":
        self.data["subject"] = {"reference": subject_ref}
        return self

    def set_occurrence(self, occurrence: str) -> "SupplyRequestBuilder":
        self.data["occurrenceDateTime"] = occurrence
        return self

    def set_requester(self, requester_ref: str) -> "SupplyRequestBuilder":
        self.data["requester"] = {"reference": requester_ref}
        return self
