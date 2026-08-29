"""Media resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class MediaBuilder(BaseBuilder):
    """Builder for Media resource."""

    def __init__(self):
        super().__init__("MediaBuilder")
        self.data = {"resourceType": "Media"}

    def set_id(self, id: str) -> "MediaBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "MediaBuilder":
        self.data["status"] = status
        return self

    def set_type(self, code: str, system: str, display: Optional[str] = None) -> "MediaBuilder":
        self.data["type"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["type"]["coding"][0]["display"] = display
        return self

    def set_modality(self, code: str, system: str, display: Optional[str] = None) -> "MediaBuilder":
        self.data["modality"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["modality"]["coding"][0]["display"] = display
        return self

    def set_subject(self, reference: str, display: Optional[str] = None) -> "MediaBuilder":
        self.data["subject"] = {"reference": reference}
        if display:
            self.data["subject"]["display"] = display
        return self

    def set_encounter(self, reference: str) -> "MediaBuilder":
        self.data["encounter"] = {"reference": reference}
        return self

    def set_created_datetime(self, created_datetime: str) -> "MediaBuilder":
        self.data["createdDateTime"] = created_datetime
        return self

    def set_extension(self, url: str, value: str) -> "MediaBuilder":
        self.data.setdefault("extension", [])
        self.data["extension"].append({"url": url, "valueString": value})
        return self

    def set_body_site(self, code: str, system: str, display: Optional[str] = None) -> "MediaBuilder":
        self.data["bodySite"] = {"coding": [{"system": system, "code": code}]}
        if display:
            self.data["bodySite"]["coding"][0]["display"] = display
        return self

    def set_content(
        self,
        content_type: str,
        data: Optional[str] = None,
        url: Optional[str] = None,
        title: Optional[str] = None,
        creation: Optional[str] = None
    ) -> "MediaBuilder":
        content: dict = {"contentType": content_type}
        if data:
            content["data"] = data
        if url:
            content["url"] = url
        if title:
            content["title"] = title
        if creation:
            content["creation"] = creation
        self.data["content"] = content
        return self

    def add_operator(self, reference: str, display: Optional[str] = None) -> "MediaBuilder":
        self.data["operator"] = {"reference": reference}
        if display:
            self.data["operator"]["display"] = display
        return self

    def add_note(self, text: str) -> "MediaBuilder":
        self.data.setdefault("note", [])
        self.data["note"].append({"text": text})
        return self
