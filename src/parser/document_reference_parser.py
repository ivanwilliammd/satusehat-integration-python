"""DocumentReferenceParser — parses FHIR DocumentReference resource."""
from __future__ import annotations

from typing import Any, Optional


class DocumentReferenceParser:
    def __init__(self, document_reference: Optional[dict[str, Any]] = None) -> None:
        self.document_reference: dict[str, Any] = (
            document_reference if isinstance(document_reference, dict) else {}
        )

    def get_identifiers(self) -> Any:
        return self.document_reference.get("identifier")

    getIdentifiers = get_identifiers

    def get_master_identifier(self) -> Any:
        return self.document_reference.get("masterIdentifier")

    getMasterIdentifier = get_master_identifier

    def get_status(self) -> Any:
        return self.document_reference.get("status")

    getStatus = get_status

    def get_doc_status(self) -> Any:
        return self.document_reference.get("docStatus")

    getDocStatus = get_doc_status

    def get_types(self) -> Any:
        return self.document_reference.get("type")

    getTypes = get_types

    def get_categories(self) -> Any:
        return self.document_reference.get("category")

    getCategories = get_categories

    def get_subject_reference(self) -> Optional[str]:
        subj = self.document_reference.get("subject")
        return subj.get("reference") if isinstance(subj, dict) else None

    getSubjectReference = get_subject_reference

    def get_date(self) -> Any:
        return self.document_reference.get("date")

    getDate = get_date

    def get_authors(self) -> Any:
        return self.document_reference.get("author")

    getAuthors = get_authors

    def get_custodian_reference(self) -> Optional[str]:
        cust = self.document_reference.get("custodian")
        return cust.get("reference") if isinstance(cust, dict) else None

    getCustodianReference = get_custodian_reference

    def get_relates_to(self) -> Any:
        return self.document_reference.get("relatesTo")

    getRelatesTo = get_relates_to

    def get_description(self) -> Any:
        return self.document_reference.get("description")

    getDescription = get_description

    def get_security_labels(self) -> Any:
        return self.document_reference.get("securityLabel")

    getSecurityLabels = get_security_labels

    def get_contents(self) -> Any:
        return self.document_reference.get("content")

    getContents = get_contents

    def get_context(self) -> Any:
        return self.document_reference.get("context")

    getContext = get_context
