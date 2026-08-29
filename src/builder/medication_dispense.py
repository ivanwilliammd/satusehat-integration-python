from src.builder.base_builder import BaseBuilder

class MedicationDispenseBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("MedicationDispense")

    def status(self, value: str) -> "MedicationDispenseBuilder":
        return self._set("status", value)

    def medication(self, codeable_concept: dict) -> "MedicationDispenseBuilder":
        return self._set("medication", codeable_concept)

    def subject(self, reference: str) -> "MedicationDispenseBuilder":
        return self._set("subject", {"reference": reference})

    def encounter(self, reference: str) -> "MedicationDispenseBuilder":
        return self._set("encounter", {"reference": reference})

    def when_prepared(self, value: str) -> "MedicationDispenseBuilder":
        return self._set("whenPrepared", value)

    def when_handed_over(self, value: str) -> "MedicationDispenseBuilder":
        return self._set("whenHandedOver", value)

    def destination(self, reference: str) -> "MedicationDispenseBuilder":
        return self._set("destination", {"reference": reference})
