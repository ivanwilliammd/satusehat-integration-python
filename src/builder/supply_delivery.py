from src.builder.base_builder import BaseBuilder


class SupplyDeliveryBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("SupplyDelivery")

    def set_status(self, status: str) -> "SupplyDeliveryBuilder":
        self.data["status"] = status
        return self

    def set_type(self, type_code: str) -> "SupplyDeliveryBuilder":
        self.data["type"] = {"coding": [{"code": type_code}]}
        return self

    def set_patient(self, patient_ref: str) -> "SupplyDeliveryBuilder":
        self.data["patient"] = {"reference": patient_ref}
        return self

    def set_encounter(self, enc_ref: str) -> "SupplyDeliveryBuilder":
        self.data["encounter"] = {"reference": enc_ref}
        return self

    def set_occurrence(self, occurrence: str) -> "SupplyDeliveryBuilder":
        self.data["occurrenceDateTime"] = occurrence
        return self

    def set_supplier(self, supplier_ref: str) -> "SupplyDeliveryBuilder":
        self.data["supplier"] = {"reference": supplier_ref}
        return self
