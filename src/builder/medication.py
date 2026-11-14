from typing import Any, Optional
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


def _arr(value: Any) -> Any:
    return value.to_array() if hasattr(value, "to_array") else value


class MedicationBuilder(BaseBuilder):
    _resourceType = "Medication"

    def __init__(self) -> None:
        super().__init__("Medication")

    def code(self, codeable_concept: dict) -> "MedicationBuilder":
        return self._set("code", codeable_concept)

    def status(self, value: str) -> "MedicationBuilder":
        return self._set("status", value)

    def manufacturer(self, display: Optional[str] = None, reference: Optional[str] = None) -> "MedicationBuilder":
        mfr: dict = {}
        if display:
            mfr["display"] = display
        if reference:
            mfr["reference"] = reference
        return self._set("manufacturer", mfr) if mfr else self

    def form(self, codeable_concept: dict) -> "MedicationBuilder":
        return self._set("form", codeable_concept)

    def ingredient(self, item_codeable_concept: dict, is_active: bool = True, strength: Optional[dict] = None) -> "MedicationBuilder":
        ing: dict = {"itemCodeableConcept": item_codeable_concept, "isActive": is_active}
        if strength:
            ing["strength"] = strength
        return self._append("ingredient", ing)

    def package(self, container: Optional[str] = None, content: Optional[List[dict]] = None) -> "MedicationBuilder":
        pkg: dict = {}
        if container:
            pkg["container"] = {"text": container}
        if content:
            pkg["content"] = content
        return self._set("package", pkg) if pkg else self

    # --- Nama kanon (cermin PayloadBuilderMedication) ---

    def set_meta_profile(self, profile: str) -> "MedicationBuilder":
        self.data.setdefault("meta", {})["profile"] = [profile]
        return self

    def set_id(self, id: str) -> "MedicationBuilder":
        return self._set("id", id)

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "MedicationBuilder":
        if value is not None:
            return self._push("identifier", {"system": identifier, "value": value})
        return self._push("identifier", _arr(identifier))

    def set_code(self, code: Any) -> "MedicationBuilder":
        return self._set("code", _arr(code))

    def set_status(self, status: str) -> "MedicationBuilder":
        return self._set("status", status)

    def set_manufacturer(self, manufacturer: Any, display: Optional[str] = None) -> "MedicationBuilder":
        if isinstance(manufacturer, str):
            ref: dict = {"reference": manufacturer}
            if display:
                ref["display"] = display
            return self._set("manufacturer", ref)
        return self._set("manufacturer", _arr(manufacturer))

    def set_form(self, form: Any) -> "MedicationBuilder":
        return self._set("form", _arr(form))

    def add_ingredient(self, item_codeable_concept: Any, is_active: bool = True,
                       strength: Any = None) -> "MedicationBuilder":
        ingredient: dict = {"itemCodeableConcept": _arr(item_codeable_concept), "isActive": is_active}
        if strength is not None:
            ingredient["strength"] = _arr(strength)
        return self._push("ingredient", ingredient)

    def set_batch(self, lot_number: str, expiration_date: str) -> "MedicationBuilder":
        return self._set("batch", {"lotNumber": lot_number, "expirationDate": expiration_date})

    def add_medication_type(self, code: str, display: str) -> "MedicationBuilder":
        # PHP memperlakukan argumen display sebagai kunci lookup, lalu jatuh ke nilai aslinya.
        opsi = {"NC": "Non-compound", "SD": "Gives of such doses", "EP": "Divide into equal parts"}
        return self._push("extension", {
            "url": "https://fhir.kemkes.go.id/r4/StructureDefinition/MedicationType",
            "valueCodeableConcept": {
                "coding": [{
                    "system": "http://terminology.kemkes.go.id/CodeSystem/medication-type",
                    "code": code,
                    "display": opsi.get(display, display),
                }],
            },
        })
