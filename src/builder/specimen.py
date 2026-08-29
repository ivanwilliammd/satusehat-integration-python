from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class SpecimenBuilder(BaseBuilder):
    _resourceType = "Specimen"

    def __init__(self) -> None:
        super().__init__("SpecimenBuilder")

    def identifier(self, system: str, value: str) -> "SpecimenBuilder":
        return self._append("identifier", {"system": system, "value": value})

    def accession_identifier(self, system: str, value: str) -> "SpecimenBuilder":
        return self._set("accessionIdentifier", {"system": system, "value": value})

    def status(self, value: str) -> "SpecimenBuilder":
        return self._set("status", value)

    def type(self, codeable_concept: dict) -> "SpecimenBuilder":
        return self._set("type", codeable_concept)

    def subject(self, reference: str, display: Optional[str] = None) -> "SpecimenBuilder":
        sub: dict = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("subject", sub)

    def received_time(self, value: str) -> "SpecimenBuilder":
        return self._set("receivedTime", value)

    def parent(self, reference: str) -> "SpecimenBuilder":
        return self._append("parent", {"reference": reference})

    def request(self, reference: str) -> "SpecimenBuilder":
        return self._append("request", {"reference": reference})

    def collection(self, collected_date_time: Optional[str] = None, collected_period: Optional[dict] = None, quantity: Optional[dict] = None, body_site: Optional[dict] = None, fasting_status: Optional[dict] = None) -> "SpecimenBuilder":
        col: dict = {}
        if collected_date_time:
            col["collectedDateTime"] = collected_date_time
        if collected_period:
            col["collectedPeriod"] = collected_period
        if quantity:
            col["quantity"] = quantity
        if body_site:
            col["bodySite"] = body_site
        if fasting_status:
            col["fastingStatus"] = fasting_status
        return self._set("collection", col) if col else self

    def processing(self, description: Optional[str] = None, procedure_codeable_concept: Optional[dict] = None, time_date_time: Optional[str] = None, time_period: Optional[dict] = None) -> "SpecimenBuilder":
        proc: dict = {}
        if description:
            proc["description"] = description
        if procedure_codeable_concept:
            proc["procedure"] = procedure_codeable_concept
        if time_date_time:
            proc["timeDateTime"] = time_date_time
        if time_period:
            proc["timePeriod"] = time_period
        return self._append("processing", proc) if proc else self

    def container(self, type_codeable_concept: Optional[dict] = None, identifier: Optional[dict] = None, specimen_quantity: Optional[dict] = None) -> "SpecimenBuilder":
        cnt: dict = {}
        if type_codeable_concept:
            cnt["type"] = type_codeable_concept
        if identifier:
            cnt["identifier"] = identifier
        if specimen_quantity:
            cnt["specimenQuantity"] = specimen_quantity
        return self._append("container", cnt) if cnt else self

    def note(self, text: str) -> "SpecimenBuilder":
        return self._append("note", {"text": text})
