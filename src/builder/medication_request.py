from typing import List, Optional
from src.builder.base_builder import BaseBuilder


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
