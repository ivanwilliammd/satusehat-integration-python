"""DocumentReference resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class DocumentReferenceBuilder(BaseBuilder):
    """Builder for DocumentReference resource."""

    def __init__(self):
        super().__init__("DocumentReference")
    def set_id(self, id: str) -> "DocumentReferenceBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "DocumentReferenceBuilder":
        self.data["status"] = status
        return self

    def set_doc_status(self, doc_status: str) -> "DocumentReferenceBuilder":
        self.data["docStatus"] = doc_status
        return self

    def set_type(self, code: str, system: str, display: Optional[str] = None) -> "DocumentReferenceBuilder":
        self.data["type"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["type"]["coding"][0]["display"] = display
        return self

    def set_category(self, code: str, system: str, display: Optional[str] = None) -> "DocumentReferenceBuilder":
        self.data["category"] = [{"coding": [{"system": system, "code": code}]}]
        if display:
            self.data["category"][0]["coding"][0]["display"] = display
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "DocumentReferenceBuilder":
        self.data["subject"] = {"reference": reference}
        if display:
            self.data["subject"]["display"] = display
        return self

    def set_date(self, date: str) -> "DocumentReferenceBuilder":
        self.data["date"] = date
        return self

    def set_description(self, description: str) -> "DocumentReferenceBuilder":
        self.data["description"] = description
        return self

    def add_security_label(self, code: str, system: str, display: Optional[str] = None) -> "DocumentReferenceBuilder":
        self.data.setdefault("securityLabel", [])
        label: dict = {"coding": [{"system": system, "code": code}]}
        if display:
            label["coding"][0]["display"] = display
        self.data["securityLabel"].append(label)
        return self

    def set_content(
        self,
        attachment_content_type: Optional[str] = None,
        attachment_data: Optional[str] = None,
        attachment_url: Optional[str] = None,
        attachment_hash: Optional[str] = None,
        attachment_title: Optional[str] = None,
        attachment_creation: Optional[str] = None
    ) -> "DocumentReferenceBuilder":
        attachment: dict = {"attachment": {}}
        att = attachment["attachment"]
        if attachment_content_type:
            att["contentType"] = attachment_content_type
        if attachment_data:
            att["data"] = attachment_data
        if attachment_url:
            att["url"] = attachment_url
        if attachment_hash:
            att["hash"] = attachment_hash
        if attachment_title:
            att["title"] = attachment_title
        if attachment_creation:
            att["creation"] = attachment_creation
        self.data["content"] = [attachment]
        return self

    def add_context_encounter(self, reference: str) -> "DocumentReferenceBuilder":
        self.data.setdefault("context", {}).setdefault("encounter", [])
        self.data["context"]["encounter"].append({"reference": reference})
        return self

    def set_context_period(self, start: Optional[str] = None, end: Optional[str] = None) -> "DocumentReferenceBuilder":
        self.data.setdefault("context", {})
        period: dict = {}
        if start:
            period["start"] = start
        if end:
            period["end"] = end
        self.data["context"]["period"] = period
        return self

    def add_author(self, reference: str, display: Optional[str] = None) -> "DocumentReferenceBuilder":
        self.data.setdefault("author", [])
        author: dict = {"reference": reference}
        if display:
            author["display"] = display
        self.data["author"].append(author)
        return self
