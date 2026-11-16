"""MedicationParser — typed accessors over the official SATUSEHAT Medication payload.

Shape source: satusehat-conformance/examples/satusehat/Medication.json, copied unchanged to
src/parser/testdata/Medication.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class MedicationParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_meta(self) -> Any:
        return self.payload.get("meta")

    getMeta = get_meta

    def get_identifier(self) -> Any:
        return self.payload.get("identifier")

    getIdentifier = get_identifier

    def get_code(self) -> Any:
        return self.payload.get("code")

    getCode = get_code

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_manufacturer(self) -> Any:
        return self.payload.get("manufacturer")

    getManufacturer = get_manufacturer

    def get_form(self) -> Any:
        return self.payload.get("form")

    getForm = get_form

    def get_ingredient(self) -> Any:
        return self.payload.get("ingredient")

    getIngredient = get_ingredient

    def get_batch(self) -> Any:
        return self.payload.get("batch")

    getBatch = get_batch

    def get_extension(self) -> Any:
        return self.payload.get("extension")

    getExtension = get_extension

    def get_package(self) -> Any:
        return self._data.get("package")

    getPackage = get_package

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id
