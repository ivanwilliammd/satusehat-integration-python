"""ErrorClassifier — classifies SATUSEHAT FHIR API HTTP responses into actionable categories."""
from __future__ import annotations

import json
from typing import Any, Optional

from .queue_interface import QueueInterface


class ErrorClassifier:
    """Maps HTTP status codes and OperationOutcome payloads to queue categories and statuses."""

    CAT_SUCCESS = "success"
    CAT_INVALID_REQUEST = "invalid_request"
    CAT_UNAUTHORIZED = "unauthorized"
    CAT_FORBIDDEN = "forbidden"
    CAT_NOT_FOUND = "not_found"
    CAT_CONFLICT = "conflict"
    CAT_VALIDATION_ERROR = "validation_error"
    CAT_RATE_LIMITED = "rate_limited"
    CAT_SERVER_ERROR = "server_error"
    CAT_NETWORK_ERROR = "network_error"
    CAT_UNEXPECTED = "unexpected"

    @classmethod
    def classify(cls, http_code: int, response_body: Any = None) -> dict[str, Any]:
        # 2xx — always success
        if 200 <= http_code < 300:
            return {
                "category": cls.CAT_SUCCESS,
                "retryable": False,
                "status": QueueInterface.STATUS_SUCCESS,
                "detail": f"HTTP {http_code}",
            }

        # 4xx ranges
        if http_code == 400:
            return {
                "category": cls.CAT_INVALID_REQUEST,
                "retryable": False,
                "status": QueueInterface.STATUS_DLQ,
                "detail": cls._extract_detail(response_body) or "Bad request (HTTP 400)",
            }

        if http_code == 401:
            return {
                "category": cls.CAT_UNAUTHORIZED,
                "retryable": True,
                "status": QueueInterface.STATUS_PENDING,
                "detail": cls._extract_detail(response_body) or "Unauthorized (HTTP 401)",
            }

        if http_code == 403:
            return {
                "category": cls.CAT_FORBIDDEN,
                "retryable": False,
                "status": QueueInterface.STATUS_DLQ,
                "detail": cls._extract_detail(response_body) or "Forbidden (HTTP 403)",
            }

        if http_code == 404:
            return {
                "category": cls.CAT_NOT_FOUND,
                "retryable": False,
                "status": QueueInterface.STATUS_DLQ,
                "detail": cls._extract_detail(response_body) or "Resource not found (HTTP 404)",
            }

        if http_code == 408:
            return {
                "category": cls.CAT_NETWORK_ERROR,
                "retryable": True,
                "status": QueueInterface.STATUS_PENDING,
                "detail": "Request timeout (HTTP 408)",
            }

        if http_code == 409:
            return {
                "category": cls.CAT_CONFLICT,
                "retryable": False,
                "status": QueueInterface.STATUS_DLQ,
                "detail": cls._extract_detail(response_body) or "Conflict (HTTP 409)",
            }

        if http_code == 412:
            return {
                "category": cls.CAT_CONFLICT,
                "retryable": False,
                "status": QueueInterface.STATUS_DLQ,
                "detail": "Precondition failed (HTTP 412) — resource changed",
            }

        if http_code == 422:
            return {
                "category": cls.CAT_VALIDATION_ERROR,
                "retryable": False,
                "status": QueueInterface.STATUS_DLQ,
                "detail": (
                    cls._extract_fhir_issues(response_body)
                    or cls._extract_detail(response_body)
                    or "Validation error (HTTP 422)"
                ),
            }

        if http_code == 429:
            return {
                "category": cls.CAT_RATE_LIMITED,
                "retryable": True,
                "status": QueueInterface.STATUS_PENDING,
                "detail": "Rate limited (HTTP 429)",
            }

        # 5xx — server errors
        if 500 <= http_code < 600:
            return {
                "category": cls.CAT_SERVER_ERROR,
                "retryable": True,
                "status": QueueInterface.STATUS_PENDING,
                "detail": f"Server error (HTTP {http_code})",
            }

        # Other 4xx
        if 400 <= http_code < 500:
            return {
                "category": cls.CAT_INVALID_REQUEST,
                "retryable": False,
                "status": QueueInterface.STATUS_DLQ,
                "detail": cls._extract_detail(response_body) or f"Client error (HTTP {http_code})",
            }

        # Fallback
        return {
            "category": cls.CAT_UNEXPECTED,
            "retryable": False,
            "status": QueueInterface.STATUS_DLQ,
            "detail": f"Unexpected HTTP {http_code}",
        }

    @classmethod
    def _extract_detail(cls, body: Any) -> Optional[str]:
        if isinstance(body, dict):
            issues = body.get("issue")
            if isinstance(issues, list) and issues and isinstance(issues[0], dict):
                diag = issues[0].get("diagnostics")
                if diag:
                    return str(diag)[:200]
            if body.get("message"):
                return str(body["message"])[:200]
            if body.get("error_description"):
                return str(body["error_description"])[:200]
        if isinstance(body, str) and body != "":
            try:
                data = json.loads(body)
                if isinstance(data, dict):
                    return cls._extract_detail(data)
            except ValueError:
                pass
            return body[:200]
        return None

    @classmethod
    def _extract_fhir_issues(cls, body: Any) -> Optional[str]:
        if isinstance(body, str) and body != "":
            try:
                body = json.loads(body)
            except ValueError:
                return None
        if not isinstance(body, dict):
            return None
        issues = body.get("issue")
        if not isinstance(issues, list) or not issues:
            return None
        lines: list[str] = []
        for issue in issues[:5]:
            if not isinstance(issue, dict):
                continue
            msg = issue.get("diagnostics") or issue.get("location") or "Unknown"
            sev = str(issue.get("severity") or "ERROR").upper()
            lines.append(f"[{sev}] {str(msg)[:100]}")
        return " | ".join(lines) if lines else None
