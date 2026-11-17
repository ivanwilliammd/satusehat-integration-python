from typing import Any, Optional
from satusehat_integration.builder.base_builder import BaseBuilder

def _arr(value: Any) -> Any:
    return value.to_array() if hasattr(value, "to_array") else value


def _reference(value: Any) -> dict:
    return {"reference": value} if isinstance(value, str) else _arr(value)


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

    # --- Nama kanon (cermin PayloadBuilderMedicationAdministration) ---

    def set_id(self, id: str) -> "MedicationAdministrationBuilder":
        return self._set("id", id)

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "MedicationAdministrationBuilder":
        if value is not None:
            return self._push("identifier", {"system": identifier, "value": value})
        return self._push("identifier", _arr(identifier))

    def set_medication_reference(self, reference: Any) -> "MedicationAdministrationBuilder":
        return self._set("medicationReference", _reference(reference))

    def set_subject(self, subject: Any) -> "MedicationAdministrationBuilder":
        return self._set("subject", _reference(subject))

    def set_context(self, context: Any) -> "MedicationAdministrationBuilder":
        return self._set("context", _reference(context))

    def set_effective_period(self, period: Any) -> "MedicationAdministrationBuilder":
        return self._set("effectivePeriod", _arr(period))

    def add_performer(self, actor: Any, display: Optional[str] = None) -> "MedicationAdministrationBuilder":
        if isinstance(actor, str):
            ref: dict = {"reference": actor}
            if display:
                ref["display"] = display
            return self._push("performer", {"actor": ref})
        return self._push("performer", {"actor": _arr(actor)})

    def add_reason_code(self, reason: Any) -> "MedicationAdministrationBuilder":
        return self._push("reasonCode", _arr(reason))

    def set_request(self, request: Any) -> "MedicationAdministrationBuilder":
        return self._set("request", _reference(request))

    def set_dosage(self, dose: Any, route: Any, site: Any) -> "MedicationAdministrationBuilder":
        dosage: dict = {}
        if dose is not None:
            dosage["dose"] = _arr(dose)
        if route is not None:
            dosage["route"] = _arr(route)
        if site is not None:
            dosage["site"] = _arr(site)
        return self._set("dosage", dosage)

    def add_contained(self, resource: dict) -> "MedicationAdministrationBuilder":
        return self._push("contained", resource)

    def set_status(self, value: str) -> "MedicationAdministrationBuilder":
        return self.status(value)
