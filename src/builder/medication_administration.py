from src.builder.base_builder import BaseBuilder

class MedicationAdministrationBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("MedicationAdministration")

    def status(self, value: str) -> "MedicationAdministrationBuilder":
        return self._set("status", value)

    def medication(self, codeable_concept: dict) -> "MedicationAdministrationBuilder":
        return self._set("medication", codeable_concept)

    def subject(self, reference: str) -> "MedicationAdministrationBuilder":
        return self._set("subject", {"reference": reference})

    def encounter(self, reference: str) -> "MedicationAdministrationBuilder":
        return self._set("encounter", {"reference": reference})

    def effective_date_time(self, value: str) -> "MedicationAdministrationBuilder":
        return self._set("effectiveDateTime", value)

    def requester(self, reference: str) -> "MedicationAdministrationBuilder":
        return self._set("requester", {"reference": reference})

    def dosage(self, dosage: dict) -> "MedicationAdministrationBuilder":
        return self._set("dosage", dosage)
