from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class MedicationBuilder(BaseBuilder):
    _resourceType = "Medication"

    def __init__(self) -> None:
        super().__init__("MedicationBuilder")

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
