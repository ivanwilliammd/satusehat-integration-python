"""QuestionnaireResponseParser — typed accessors over the official SATUSEHAT QuestionnaireResponse payload.

Shape source: satusehat-conformance/examples/satusehat/QuestionnaireResponse.json, copied unchanged to
satusehat_integration/parser/testdata/QuestionnaireResponse.json. One accessor per element the official example contains;
get_raw() always returns the payload so a caller is never blocked by a missing accessor.
"""
from __future__ import annotations

from typing import Any, Optional


class QuestionnaireResponseParser:
    def __init__(self, payload: Optional[dict[str, Any]] = None) -> None:
        self.payload: dict[str, Any] = payload if isinstance(payload, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self.payload

    def get_resource_type(self) -> Any:
        return self.payload.get("resourceType")

    getResourceType = get_resource_type

    def get_questionnaire(self) -> Any:
        return self.payload.get("questionnaire")

    getQuestionnaire = get_questionnaire

    def get_status(self) -> Any:
        return self.payload.get("status")

    getStatus = get_status

    def get_subject(self) -> Any:
        return self.payload.get("subject")

    getSubject = get_subject

    def get_encounter(self) -> Any:
        return self.payload.get("encounter")

    getEncounter = get_encounter

    def get_authored(self) -> Any:
        return self.payload.get("authored")

    getAuthored = get_authored

    def get_author(self) -> Any:
        return self.payload.get("author")

    getAuthor = get_author

    def get_source(self) -> Any:
        return self.payload.get("source")

    getSource = get_source

    def get_item(self) -> Any:
        return self.payload.get("item")

    getItem = get_item
