"""CareTeam resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from .base import BaseBuilder


class CareTeamBuilder(BaseBuilder):
    """Builder for CareTeam resource."""

    def __init__(self):
        super().__init__()
        self._data = {"resourceType": "CareTeam"}

    def set_id(self, id: str) -> "CareTeamBuilder":
        self._data["id"] = id
        return self

    def set_status(self, status: str) -> "CareTeamBuilder":
        self._data["status"] = status
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "CareTeamBuilder":
        self._data["subject"] = {"reference": reference}
        if display:
            self._data["subject"]["display"] = display
        return self

    def set_period(self, start: Optional[str] = None, end: Optional[str] = None) -> "CareTeamBuilder":
        period: dict = {}
        if start:
            period["start"] = start
        if end:
            period["end"] = end
        self._data["period"] = period
        return self

    def add_category(self, code: str, system: str, display: Optional[str] = None) -> "CareTeamBuilder":
        self._data.setdefault("category", [])
        cat: dict = {"coding": [{"system": system, "code": code}]}
        if display:
            cat["coding"][0]["display"] = display
        self._data["category"].append(cat)
        return self

    def add_participant(
        self,
        role_code: Optional[str] = None,
        role_system: Optional[str] = None,
        role_display: Optional[str] = None,
        member_reference: Optional[str] = None,
        member_display: Optional[str] = None
    ) -> "CareTeamBuilder":
        self._data.setdefault("participant", [])
        participant: dict = {}
        if role_code:
            participant["role"] = {"coding": [{"code": role_code}]}
            if role_system:
                participant["role"]["coding"][0]["system"] = role_system
            if role_display:
                participant["role"]["coding"][0]["display"] = role_display
        if member_reference:
            participant["member"] = {"reference": member_reference}
            if member_display:
                participant["member"]["display"] = member_display
        self._data["participant"].append(participant)
        return self

    def add_reason_code(self, code: str, system: str, display: Optional[str] = None) -> "CareTeamBuilder":
        self._data.setdefault("reasonCode", [])
        rc: dict = {"coding": [{"system": system, "code": code}]}
        if display:
            rc["coding"][0]["display"] = display
        self._data["reasonCode"].append(rc)
        return self

    def add_note(self, text: str) -> "CareTeamBuilder":
        self._data.setdefault("note", [])
        self._data["note"].append({"text": text})
        return self
