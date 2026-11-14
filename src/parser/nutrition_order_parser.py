"""NutritionOrderParser — typed accessors over the official SATUSEHAT NutritionOrder payload.

Shape source: satusehat-conformance/examples/satusehat/NutritionOrder.json, copied unchanged to
src/parser/testdata/NutritionOrder.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class NutritionOrderParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_identifier(self) -> Any:
        return self.payload.get("identifier")

    getIdentifier = get_identifier

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_intent(self) -> Any:
        return self.payload.get("intent")

    getIntent = get_intent

    def get_patient(self) -> Any:
        return self.payload.get("patient")

    getPatient = get_patient

    def get_encounter(self) -> Any:
        return self.payload.get("encounter")

    getEncounter = get_encounter

    def get_date_time(self) -> Any:
        return self.payload.get("dateTime")

    getDateTime = get_date_time

    def get_oral_diet(self) -> Any:
        return self.payload.get("oralDiet")

    getOralDiet = get_oral_diet
