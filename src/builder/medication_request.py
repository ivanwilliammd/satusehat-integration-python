from typing import List, Optional
from src.builder.base_builder import BaseBuilder
from typing import Any


def _arr(value: Any) -> Any:
    return value.to_array() if hasattr(value, "to_array") else value


class MedicationRequestBuilder(BaseBuilder):
    _resourceType = "MedicationRequest"

    def __init__(self) -> None:
        super().__init__("MedicationRequest")

    def status(self, value: str) -> "MedicationRequestBuilder":
        return self._set("status", value)

    def intent(self, value: str) -> "MedicationRequestBuilder":
        return self._set("intent", value)

    def subject(self, reference: str, display: Optional[str] = None) -> "MedicationRequestBuilder":
        subj: dict = {"reference": reference}
        if display:
            subj["display"] = display
        return self._set("subject", subj)

    def encounter(self, reference: str) -> "MedicationRequestBuilder":
        return self._set("encounter", {"reference": reference})

    def authored_on(self, value: str) -> "MedicationRequestBuilder":
        return self._set("authoredOn", value)

    def requester(self, reference: str, display: Optional[str] = None) -> "MedicationRequestBuilder":
        req: dict = {"reference": reference}
        if display:
            req["display"] = display
        return self._set("requester", req)

    def medication(self, codeable_concept: dict) -> "MedicationRequestBuilder":
        return self._set("medicationCodeableConcept", codeable_concept)

    def medication_reference(self, reference: str) -> "MedicationRequestBuilder":
        return self._set("medicationReference", {"reference": reference})

    def dosage_instruction(self, text: Optional[str] = None, timing_repeat: Optional[dict] = None, dose_quantity: Optional[dict] = None) -> "MedicationRequestBuilder":
        di: dict = {}
        if text:
            di["text"] = text
        if timing_repeat:
            di["timing"] = {"repeat": timing_repeat}
        if dose_quantity:
            di["doseAndRate"] = [{"doseQuantity": dose_quantity}]
        return self._append("dosageInstruction", di)

    def dispense_request(self, validity_period: Optional[dict] = None, number_of_repeats: Optional[int] = None, quantity: Optional[dict] = None, expected_supply_duration: Optional[dict] = None) -> "MedicationRequestBuilder":
        dr: dict = {}
        if validity_period:
            dr["validityPeriod"] = validity_period
        if number_of_repeats is not None:
            dr["numberOfRepeatsAllowed"] = number_of_repeats
        if quantity:
            dr["quantity"] = quantity
        if expected_supply_duration:
            dr["expectedSupplyDuration"] = expected_supply_duration
        return self._set("dispenseRequest", dr) if dr else self

    def dosage_additional_instruction(self, text: str) -> "MedicationRequestBuilder":
        return self._append("dosageInstruction", {"additionalInstruction": [{"text": text}]})

    # --- Nama kanon (cermin PayloadBuilderMedicationRequest) ---

    def set_id(self, id: str) -> "MedicationRequestBuilder":
        return self._set("id", id)

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "MedicationRequestBuilder":
        if value is not None:
            return self._push("identifier", {"system": identifier, "value": value})
        return self._push("identifier", _arr(identifier))

    def add_category(self, category: Any) -> "MedicationRequestBuilder":
        return self._push("category", _arr(category))

    def set_medication_codeable_concept(self, medication: Any) -> "MedicationRequestBuilder":
        return self._set("medicationCodeableConcept", _arr(medication))

    def set_medication_reference(self, medication: Any) -> "MedicationRequestBuilder":
        if isinstance(medication, str):
            return self._set("medicationReference", {"reference": medication})
        return self._set("medicationReference", _arr(medication))

    def set_recorder(self, recorder: Any, display: Optional[str] = None) -> "MedicationRequestBuilder":
        if isinstance(recorder, str):
            ref: dict = {"reference": recorder}
            if display:
                ref["display"] = display
            return self._set("recorder", ref)
        return self._set("recorder", _arr(recorder))

    def add_reason_code(self, reason_code: Any) -> "MedicationRequestBuilder":
        return self._push("reasonCode", _arr(reason_code))

    def add_reason_reference(self, reason_reference: Any) -> "MedicationRequestBuilder":
        return self._push("reasonReference", _arr(reason_reference))

    def add_dosage_instruction(self, dosage: Any) -> "MedicationRequestBuilder":
        return self._push("dosageInstruction", _arr(dosage))

    def set_dispense_request(
        self,
        validity_period: Any = None,
        number_of_repeats_allowed: Optional[int] = None,
        quantity: Any = None,
        expected_supply_duration: Any = None,
        performer: Any = None,
    ) -> "MedicationRequestBuilder":
        dispense: dict = {}
        if validity_period is not None:
            dispense["validityPeriod"] = _arr(validity_period)
        if number_of_repeats_allowed is not None:
            dispense["numberOfRepeatsAllowed"] = number_of_repeats_allowed
        if quantity is not None:
            dispense["quantity"] = _arr(quantity)
        if expected_supply_duration is not None:
            dispense["expectedSupplyDuration"] = _arr(expected_supply_duration)
        if performer is not None:
            dispense["performer"] = _arr(performer)
        return self._set("dispenseRequest", dispense)

    def set_dispense_interval(self, dispense_interval: Any) -> "MedicationRequestBuilder":
        dispense = dict(self.data.get("dispenseRequest") or {})
        dispense["dispenseInterval"] = _arr(dispense_interval)
        return self._set("dispenseRequest", dispense)

    def set_initial_fill(self, initial_fill: Any) -> "MedicationRequestBuilder":
        dispense = dict(self.data.get("dispenseRequest") or {})
        dispense["initialFill"] = _arr(initial_fill)
        return self._set("dispenseRequest", dispense)

    def set_substitution(self, substitution: Any, allowed: Optional[bool] = None) -> "MedicationRequestBuilder":
        row: dict = {"code": _arr(substitution)}
        if allowed is not None:
            row["allowedBoolean"] = allowed
        return self._set("substitution", row)

    def add_prior_prescription(self, prior_prescription: Any) -> "MedicationRequestBuilder":
        return self._push("priorPrescription", _arr(prior_prescription))

    def add_detected_issue(self, detected_issue: Any) -> "MedicationRequestBuilder":
        return self._push("detectedIssue", _arr(detected_issue))

    def add_event_history(self, event_history: Any) -> "MedicationRequestBuilder":
        return self._push("eventHistory", _arr(event_history))

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "MedicationRequestBuilder":
        extension: dict = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        return self._push("extension", extension)

    def set_status(self, value: str) -> "MedicationRequestBuilder":
        return self.status(value)

    def set_intent(self, value: str) -> "MedicationRequestBuilder":
        return self.intent(value)

    def set_subject(self, value: str) -> "MedicationRequestBuilder":
        return self.subject(value)

    def set_encounter(self, value: str) -> "MedicationRequestBuilder":
        return self.encounter(value)

    def set_authored_on(self, value: str) -> "MedicationRequestBuilder":
        return self.authored_on(value)

    def set_requester(self, value: str) -> "MedicationRequestBuilder":
        return self.requester(value)
