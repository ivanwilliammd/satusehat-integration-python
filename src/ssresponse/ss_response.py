"""SSResponse — wraps HTTP response from SATUSEHAT FHIR API."""
from __future__ import annotations

from typing import Any, Optional


class SSResponse:
    """Wraps an HTTP response from SATUSEHAT with convenience extractors."""

    def __init__(self, http_code: int, body: Optional[dict[str, Any]] = None, content: str = "") -> None:
        self._http_code = int(http_code)
        self._body: dict[str, Any] = body if isinstance(body, dict) else {}
        self._content = str(content)

    @property
    def http_code(self) -> int:
        return self._http_code

    @property
    def body(self) -> dict[str, Any]:
        return self._body

    @property
    def content(self) -> str:
        return self._content

    def get_http_code(self) -> int:
        return self._http_code

    getHttpCode = get_http_code

    def get_body(self) -> dict[str, Any]:
        return self._body

    getBody = get_body

    def get_content(self) -> str:
        return self._content

    getContent = get_content

    def is_success(self) -> bool:
        return 200 <= self._http_code < 300

    isSuccess = is_success

    def is_error(self) -> bool:
        return not self.is_success()

    isError = is_error

    def get_error_messages(self) -> list[str]:
        """Extract FHIR OperationOutcome issue messages from response body."""
        messages: list[str] = []

        if self._body.get("resourceType") != "OperationOutcome":
            return messages

        issues = self._body.get("issue")
        if not isinstance(issues, list):
            return messages

        for issue in issues:
            if not isinstance(issue, dict):
                continue
            details = issue.get("details")
            text = None
            if isinstance(details, dict):
                text = details.get("text")
            if not text:
                text = issue.get("diagnostics")
            if not text and isinstance(details, dict):
                codings = details.get("coding")
                if isinstance(codings, list) and codings and isinstance(codings[0], dict):
                    text = codings[0].get("display")

            if text:
                messages.append(str(text))

        return messages

    getErrorMessages = get_error_messages

    def get_resource_id(self) -> Optional[str]:
        """Extract resource id from response body."""
        res_id = self._body.get("id")
        if res_id:
            return str(res_id)

        # Bundle entry link (self link contains full URL with id)
        if self._body.get("resourceType") == "Bundle":
            link = self._body.get("link")
            self_link = None
            if isinstance(link, dict):
                self_obj = link.get("self")
                if isinstance(self_obj, dict):
                    self_link = self_obj.get("url")
            if self_link:
                parts = str(self_link).split("/")
                id_part = parts[-1].split("?")[0]
                if id_part != "":
                    return id_part

            entries = self._body.get("entry")
            if isinstance(entries, list) and entries and isinstance(entries[0], dict):
                resource = entries[0].get("resource")
                if isinstance(resource, dict) and resource.get("id"):
                    return str(resource["id"])

        # Patient create response
        if self._body.get("success") is True:
            data = self._body.get("data")
            if isinstance(data, dict) and data.get("patient_id"):
                return str(data["patient_id"])

        create_patient = self._body.get("create_patient")
        if isinstance(create_patient, dict) and create_patient.get("success") is True:
            data = create_patient.get("data")
            if isinstance(data, dict) and data.get("patient_id"):
                return str(data["patient_id"])

        return None

    getResourceId = get_resource_id

    def get(self, resource_type: str = "") -> Optional[str]:
        """Shorthand for get_resource_id — returns the id of the given FHIR resource type."""
        _ = resource_type
        return self.get_resource_id()
