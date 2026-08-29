"""Contract resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from .base import BaseBuilder


class ContractBuilder(BaseBuilder):
    """Builder for Contract resource."""

    def __init__(self):
        super().__init__()
        self._data = {"resourceType": "Contract"}

    def set_id(self, id: str) -> "ContractBuilder":
        self._data["id"] = id
        return self

    def set_status(self, status: str) -> "ContractBuilder":
        self._data["status"] = status
        return self

    def set_issued(self, issued: str) -> "ContractBuilder":
        self._data["issued"] = issued
        return self

    def set_applies(self, start: Optional[str] = None, end: Optional[str] = None) -> "ContractBuilder":
        period: dict = {}
        if start:
            period["start"] = start
        if end:
            period["end"] = end
        self._data["applies"] = period
        return self

    def add_type(self, code: str, system: str, display: Optional[str] = None) -> "ContractBuilder":
        self._data.setdefault("type", [])
        t: dict = {"coding": [{"system": system, "code": code}]}
        if display:
            t["coding"][0]["display"] = display
        self._data["type"].append(t)
        return self

    def add_subject(self, reference: str, display: Optional[str] = None) -> "ContractBuilder":
        self._data.setdefault("subject", [])
        subj: dict = {"reference": reference}
        if display:
            subj["display"] = display
        self._data["subject"].append(subj)
        return self

    def add_authority(self, reference: str, display: Optional[str] = None) -> "ContractBuilder":
        self._data.setdefault("authority", [])
        auth: dict = {"reference": reference}
        if display:
            auth["display"] = display
        self._data["authority"].append(auth)
        return self

    def add_domain(self, reference: str, display: Optional[str] = None) -> "ContractBuilder":
        self._data.setdefault("domain", [])
        dom: dict = {"reference": reference}
        if display:
            dom["display"] = display
        self._data["domain"].append(dom)
        return self

    def add_legal(
        self,
        content_reference: Optional[str] = None,
        text: Optional[str] = None
    ) -> "ContractBuilder":
        self._data.setdefault("legal", [])
        legal: dict = {}
        if content_reference:
            legal["contentAttachment"] = {"reference": content_reference}
        if text:
            legal["contentAttachment"] = legal.get("contentAttachment", {})
            legal["contentAttachment"]["contentString"] = text
        self._data["legal"].append(legal)
        return self

    def add_rule(
        self,
        content_reference: Optional[str] = None,
        text: Optional[str] = None
    ) -> "ContractBuilder":
        self._data.setdefault("rule", [])
        r: dict = {}
        if content_reference:
            r["contentAttachment"] = {"reference": content_reference}
        if text:
            r["contentAttachment"] = r.get("contentAttachment", {})
            r["contentAttachment"]["contentString"] = text
        self._data["rule"].append(r)
        return self

    def add_agent(
        self,
        actor_reference: str,
        role_code: Optional[str] = None,
        role_system: Optional[str] = None,
        role_display: Optional[str] = None
    ) -> "ContractBuilder":
        self._data.setdefault("agent", [])
        agent: dict = {"actor": {"reference": actor_reference}}
        if role_code:
            agent["role"] = {"coding": [{"code": role_code}]}
            if role_system:
                agent["role"]["coding"][0]["system"] = role_system
            if role_display:
                agent["role"]["coding"][0]["display"] = role_display
        self._data["agent"].append(agent)
        return self

    def add_signer(
        self,
        type_code: str,
        type_system: str,
        party_reference: str,
        party_display: Optional[str] = None
    ) -> "ContractBuilder":
        self._data.setdefault("signer", [])
        signer: dict = {
            "type": {"coding": [{"code": type_code, "system": type_system}]},
            "party": {"reference": party_reference}
        }
        if party_display:
            signer["party"]["display"] = party_display
        self._data["signer"].append(signer)
        return self
