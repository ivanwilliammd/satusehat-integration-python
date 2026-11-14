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

    # --- Nama kanon (cermin PayloadBuilderDocumentReference) ---

    def _arr(self, value: Any) -> Any:
        return value.to_array() if hasattr(value, "to_array") else value

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "DocumentReferenceBuilder":
        entry = {"system": identifier, "value": value} if value is not None else self._arr(identifier)
        self.data.setdefault("identifier", []).append(entry)
        return self

    def set_master_identifier(self, master_identifier: Any, value: Optional[str] = None) -> "DocumentReferenceBuilder":
        if value is not None:
            self.data["masterIdentifier"] = {"system": master_identifier, "value": value}
        else:
            self.data["masterIdentifier"] = self._arr(master_identifier)
        return self

    def add_type(self, doc_type: Any) -> "DocumentReferenceBuilder":
        # PHP menulis type sebagai daftar walau FHIR menyebut 0..1.
        self.data.setdefault("type", []).append(self._arr(doc_type))
        return self

    def add_category(self, category: Any) -> "DocumentReferenceBuilder":
        self.data.setdefault("category", []).append(self._arr(category))
        return self

    def set_custodian(self, custodian: Any) -> "DocumentReferenceBuilder":
        entry = {"reference": custodian} if isinstance(custodian, str) else self._arr(custodian)
        self.data["custodian"] = entry
        return self

    def add_relates_to(self, code: str, target: Any) -> "DocumentReferenceBuilder":
        entry = {"reference": target} if isinstance(target, str) else self._arr(target)
        self.data.setdefault("relatesTo", []).append({"code": code, "target": entry})
        return self

    def add_security_label_canonical(self, security_label: Any) -> "DocumentReferenceBuilder":
        """Bentuk kanon: menerima CodeableConcept siap pakai."""
        self.data.setdefault("securityLabel", []).append(self._arr(security_label))
        return self

    def add_content(self, attachment: Any, format: Any = None) -> "DocumentReferenceBuilder":
        row: Dict[str, Any] = {"attachment": self._arr(attachment)}
        if format is not None:
            row["format"] = self._arr(format)
        self.data.setdefault("content", []).append(row)
        return self

    def set_context(self, context: Dict[str, Any]) -> "DocumentReferenceBuilder":
        self.data["context"] = context
        return self

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "DocumentReferenceBuilder":
        extension: Dict[str, Any] = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        self.data.setdefault("extension", []).append(extension)
        return self
