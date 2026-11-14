"""CompositionParser — typed accessors over the official SATUSEHAT Composition payload.

Shape source: satusehat-conformance/examples/satusehat/Composition.json, copied unchanged to
src/parser/testdata/Composition.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class CompositionParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_attester(self) -> Any:
        return self.payload.get("attester")

    getAttester = get_attester

    def get_type(self) -> Any:
        return self.payload.get("type")

    getType = get_type

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_encounter(self) -> Any:
        return self.payload.get("encounter")

    getEncounter = get_encounter

    def get_date(self) -> Any:
        return self.payload.get("date")

    getDate = get_date

    def get_author(self) -> Any:
        return self.payload.get("author")

    getAuthor = get_author

    def get_title(self) -> Any:
        return self.payload.get("title")

    getTitle = get_title

    def get_section(self) -> Any:
        return self.payload.get("section")

    getSection = get_section
