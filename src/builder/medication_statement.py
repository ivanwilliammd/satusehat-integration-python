from src.builder.base_builder import BaseBuilder

class MedicationStatementBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("MedicationStatementBuilder")

    def status(self, value: str) -> "MedicationStatementBuilder":
        return self._set("status", value)

    def medication(self, codeable_concept: dict) -> "MedicationStatementBuilder":
        return self._set("medication", codeable_concept)

    def subject(self, reference: str) -> "MedicationStatementBuilder":
        return self._set("subject", {"reference": reference})

    def effective_date_time(self, value: str) -> "MedicationStatementBuilder":
        return self._set("effectiveDateTime", value)

    def date_asserted(self, value: str) -> "MedicationStatementBuilder":
        return self._set("dateAsserted", value)

    def information_source(self, reference: str) -> "MedicationStatementBuilder":
        return self._set("informationSource", {"reference": reference})

    def dosage(self, dosage: dict) -> "MedicationStatementBuilder":
        return self._push("dosage", dosage)
