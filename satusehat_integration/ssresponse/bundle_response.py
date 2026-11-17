"""BundleResponse — parses FHIR Bundle responses (batch-response / transaction-response)."""
from __future__ import annotations

from typing import Any, Optional


class BundleResponse:
    """Parses FHIR Bundle responses and correlates with request entries."""

    def __init__(
        self,
        http_code: int,
        bundle: Optional[dict[str, Any]] = None,
        request_entries: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        self._http_code = int(http_code)
        self._bundle: dict[str, Any] = bundle if isinstance(bundle, dict) else {}
        self._request_entries: list[dict[str, Any]] = list(request_entries) if request_entries else []

    def get_http_code(self) -> int:
        return self._http_code

    getHttpCode = get_http_code

    def get_bundle(self) -> dict[str, Any]:
        return self._bundle

    getBundle = get_bundle

    def is_success(self) -> bool:
        return 200 <= self._http_code < 300

    isSuccess = is_success

    def get_total(self) -> int:
        return int(self._bundle.get("total") or 0)

    getTotal = get_total

    # -------------------------------------------------------------------------
    # Entry helpers (raw — no request context)
    # -------------------------------------------------------------------------

    def get_entries(self) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        raw_entries = self._bundle.get("entry")
        if not isinstance(raw_entries, list):
            return entries

        for entry in raw_entries:
            if not isinstance(entry, dict):
                continue
            response = entry.get("response") if isinstance(entry.get("response"), dict) else {}
            entries.append(
                {
                    "status": response.get("status", ""),
                    "location": response.get("location", ""),
                    "etag": response.get("etag", ""),
                    "lastModified": response.get("lastModified", ""),
                    "outcome": response.get("outcome"),
                    "fullUrl": entry.get("fullUrl", ""),
                }
            )
        return entries

    getEntries = get_entries

    def get_entry_statuses(self) -> list[str]:
        return [str(entry["status"]) for entry in self.get_entries()]

    getEntryStatuses = get_entry_statuses

    @staticmethod
    def _parse_status_code(status: str) -> int:
        if not status:
            return 0
        part = str(status).split(" ")[0]
        try:
            return int(part)
        except ValueError:
            return 0

    def get_success_entries(self) -> list[dict[str, Any]]:
        success: list[dict[str, Any]] = []
        for index, entry in enumerate(self.get_entries()):
            code = self._parse_status_code(entry["status"])
            if 200 <= code < 300:
                success.append({"index": index, **entry})
        return success

    getSuccessEntries = get_success_entries

    def get_failed_entries(self) -> list[dict[str, Any]]:
        failed: list[dict[str, Any]] = []
        for index, entry in enumerate(self.get_entries()):
            code = self._parse_status_code(entry["status"])
            if code >= 400 or code == 0:
                failed.append({"index": index, **entry})
        return failed

    getFailedEntries = get_failed_entries

    def get_entry_resource_id(self, index: int) -> Optional[str]:
        entries = self._bundle.get("entry")
        if not isinstance(entries, list) or index < 0 or index >= len(entries):
            return None
        entry = entries[index]
        if not isinstance(entry, dict):
            return None
        response = entry.get("response")
        location = response.get("location", "") if isinstance(response, dict) else ""
        if not location:
            return None
        parts = str(location).split("/")
        id_part = parts[-1].split("?")[0]
        return id_part if id_part != "" else None

    getEntryResourceId = get_entry_resource_id

    def get_entry_errors(self, index: int) -> list[str]:
        entries = self._bundle.get("entry")
        if not isinstance(entries, list) or index < 0 or index >= len(entries):
            return []
        entry = entries[index]
        if not isinstance(entry, dict):
            return []
        response = entry.get("response")
        outcome = response.get("outcome") if isinstance(response, dict) else None
        if not isinstance(outcome, dict) or outcome.get("resourceType") != "OperationOutcome":
            return []

        issues = outcome.get("issue")
        if not isinstance(issues, list):
            return []

        messages: list[str] = []
        for issue in issues:
            if not isinstance(issue, dict):
                continue
            details = issue.get("details")
            text = details.get("text") if isinstance(details, dict) else None
            if not text:
                text = issue.get("diagnostics")
            if not text and isinstance(details, dict):
                codings = details.get("coding")
                if isinstance(codings, list) and codings and isinstance(codings[0], dict):
                    text = codings[0].get("display")
            if text:
                messages.append(str(text))
        return messages

    getEntryErrors = get_entry_errors

    def get_resource_ids(self) -> list[dict[str, Any]]:
        ids: list[dict[str, Any]] = []
        for index, entry in enumerate(self.get_entries()):
            res_id = self.get_entry_resource_id(index)
            if res_id:
                ids.append(
                    {
                        "fullUrl": entry["fullUrl"],
                        "id": res_id,
                        "location": entry["location"],
                    }
                )
        return ids

    getResourceIds = get_resource_ids

    def is_all_success(self) -> bool:
        entries = self.get_entries()
        if not entries:
            return False
        for entry in entries:
            code = self._parse_status_code(str(entry["status"]))
            if code < 200 or code >= 300:
                return False
        return True

    isAllSuccess = is_all_success

    # -------------------------------------------------------------------------
    # Request-context helpers
    # -------------------------------------------------------------------------

    def by_method(self, methods: list[str]) -> list[dict[str, Any]]:
        if not self._request_entries:
            return []

        upper_methods = {m.upper() for m in methods}
        results: list[dict[str, Any]] = []
        response_entries = self._bundle.get("entry") if isinstance(self._bundle.get("entry"), list) else []

        for req_index, req_entry in enumerate(self._request_entries):
            req_dict = req_entry.get("request", req_entry) if isinstance(req_entry, dict) else {}
            method = str(req_entry.get("method") or req_dict.get("method") or "").upper()
            if method not in upper_methods:
                continue

            resp_entry = response_entries[req_index] if req_index < len(response_entries) and isinstance(response_entries[req_index], dict) else {}
            response = resp_entry.get("response") if isinstance(resp_entry.get("response"), dict) else {}
            status = str(response.get("status", ""))
            status_code = self._parse_status_code(status)
            location = str(response.get("location", ""))

            resource_id = None
            if location != "":
                parts = location.split("/")
                id_part = parts[-1].split("?")[0]
                if id_part != "":
                    resource_id = id_part

            errors: list[str] = []
            outcome = response.get("outcome")
            if isinstance(outcome, dict) and outcome.get("resourceType") == "OperationOutcome":
                for issue in outcome.get("issue") or []:
                    if not isinstance(issue, dict):
                        continue
                    details = issue.get("details")
                    text = details.get("text") if isinstance(details, dict) else None
                    if not text:
                        text = issue.get("diagnostics")
                    if not text and isinstance(details, dict):
                        codings = details.get("coding")
                        if isinstance(codings, list) and codings and isinstance(codings[0], dict):
                            text = codings[0].get("display")
                    if text:
                        errors.append(str(text))

            resource = resp_entry.get("resource") if method == "GET" and "resource" in resp_entry else None
            url = req_entry.get("url") or req_dict.get("url") or ""

            results.append(
                {
                    "index": req_index,
                    "method": method,
                    "url": url,
                    "fullUrl": req_entry.get("fullUrl", ""),
                    "status": status,
                    "statusCode": status_code,
                    "location": location,
                    "resourceId": resource_id,
                    "etag": response.get("etag", ""),
                    "lastModified": response.get("lastModified", ""),
                    "outcome": outcome,
                    "errors": errors,
                    "isSuccess": 200 <= status_code < 300,
                    "resource": resource,
                }
            )
        return results

    byMethod = by_method

    def created(self) -> list[dict[str, Any]]:
        return self.by_method(["POST"])

    def updated(self) -> list[dict[str, Any]]:
        return self.by_method(["PUT"])

    def patched(self) -> list[dict[str, Any]]:
        return self.by_method(["PATCH"])

    def read(self) -> list[dict[str, Any]]:
        return self.by_method(["GET"])

    def deleted(self) -> list[dict[str, Any]]:
        return self.by_method(["DELETE"])

    def id_map(self) -> dict[str, str]:
        mapping: dict[str, str] = {}
        for entry in self.created():
            if entry.get("fullUrl") and entry.get("resourceId"):
                mapping[str(entry["fullUrl"])] = str(entry["resourceId"])
        return mapping

    idMap = id_map

    def find(self, resource_type: str, resource_id: str) -> Optional[dict[str, Any]]:
        response_entries = self._bundle.get("entry") if isinstance(self._bundle.get("entry"), list) else []
        rt_lower = resource_type.lower()
        rid_lower = resource_id.lower()

        for req_index, req_entry in enumerate(self._request_entries):
            req_dict = req_entry.get("request", req_entry) if isinstance(req_entry, dict) else {}
            url = str(req_entry.get("url") or req_dict.get("url") or "")
            if rt_lower in url.lower() and rid_lower in url.lower():
                resp_entry = (
                    response_entries[req_index].get("response", {})
                    if req_index < len(response_entries) and isinstance(response_entries[req_index], dict)
                    else {}
                )
                status = str(resp_entry.get("status", ""))
                code = self._parse_status_code(status)
                return {
                    "index": req_index,
                    "method": req_entry.get("method") or req_dict.get("method") or "",
                    "status": status,
                    "statusCode": code,
                    "location": resp_entry.get("location", ""),
                    "resourceId": self.get_entry_resource_id(req_index),
                    "isSuccess": code >= 200,
                }
        return None
