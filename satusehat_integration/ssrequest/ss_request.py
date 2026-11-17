"""SSRequest — FHIR R4 HTTP client with automatic token refresh and retry backoff."""
from __future__ import annotations

import json
import time
from typing import Any, Callable, Optional, Union
from urllib.parse import urlencode

import requests

from ..ssresponse.ss_response import SSResponse
from .oauth2_client import OAuth2Client


class SSRequest:
    """HTTP client for SATUSEHAT FHIR R4 API with retry and token refresh support."""

    def __init__(
        self,
        oauth2: Optional[OAuth2Client] = None,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
        config: Optional[dict[str, Any]] = None,
        session: Optional[requests.Session] = None,
        sleep_fn: Optional[Callable[[float], None]] = None,
    ) -> None:
        self._oauth2 = oauth2
        self._token = token
        self._config: dict[str, Any] = {"log_enabled": True, **(config or {})}
        self._timeout = int(self._config.get("timeout", 30))
        self._max_retries = int(self._config.get("maxRetries", self._config.get("max_retries", 5)))
        self._verify = bool(self._config.get("verify", True))
        self._retry_count = 0
        self._sleep_fn = sleep_fn or time.sleep

        self._default_headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/fhir+json",
        }
        extra_headers = self._config.get("headers")
        if isinstance(extra_headers, dict):
            self._default_headers.update(extra_headers)

        if base_url is not None:
            self._base_url = base_url.rstrip("/")
        elif oauth2 is not None and getattr(oauth2, "fhir_url", None):
            self._base_url = str(oauth2.fhir_url).rstrip("/")
        else:
            self._base_url = ""

        self._session = session or requests.Session()

    # -------------------------------------------------------------------------
    # Public HTTP methods
    # -------------------------------------------------------------------------

    def get(self, url: str, params: Optional[dict[str, Any]] = None) -> SSResponse:
        full_url = self._build_url(url, params)
        return self._request("GET", full_url)

    def post(self, url: str, body: Union[dict[str, Any], list[Any]]) -> SSResponse:
        full_url = self._build_url(url)
        return self._request("POST", full_url, body)

    def put(self, url: str, body: Union[dict[str, Any], list[Any]]) -> SSResponse:
        full_url = self._build_url(url)
        return self._request("PUT", full_url, body)

    def delete(self, url: str, body: Optional[Union[dict[str, Any], list[Any]]] = None) -> SSResponse:
        full_url = self._build_url(url)
        return self._request("DELETE", full_url, body)

    def patch(self, url: str, patch_payload: Union[dict[str, Any], list[Any]]) -> SSResponse:
        full_url = self._build_url(url)
        return self._request("PATCH", full_url, patch_payload)

    def patch_fhir_path(self, url: str, fhir_path_payload: Union[dict[str, Any], list[Any]]) -> SSResponse:
        full_url = self._build_url(url)
        self._retry_count = 0
        return self._do_request("PATCH", full_url, fhir_path_payload, "application/fhir+json")

    patchFhirPath = patch_fhir_path

    def post_bundle(self, url: str, bundle_payload: dict[str, Any]) -> SSResponse:
        return self.post(url, bundle_payload)

    postBundle = post_bundle

    # -------------------------------------------------------------------------
    # Token resolution
    # -------------------------------------------------------------------------

    def _get_token(self) -> Optional[str]:
        if self._token is not None:
            return self._token
        if self._oauth2 is not None:
            tok = self._oauth2.token()
            return tok if isinstance(tok, str) else None
        return None

    def _should_auto_refresh(self) -> bool:
        if self._oauth2 is not None:
            fn = getattr(self._oauth2, "is_token_auto_refresh", None) or getattr(
                self._oauth2, "isTokenAutoRefresh", None
            )
            if callable(fn):
                return bool(fn())
        return False

    # -------------------------------------------------------------------------
    # Core request with retry logic
    # -------------------------------------------------------------------------

    def _request(
        self,
        method: str,
        url: str,
        body: Optional[Union[dict[str, Any], list[Any]]] = None,
    ) -> SSResponse:
        self._retry_count = 0
        return self._do_request(method, url, body)

    def _do_request(
        self,
        method: str,
        url: str,
        body: Optional[Union[dict[str, Any], list[Any]]] = None,
        content_type: Optional[str] = None,
    ) -> SSResponse:
        token = self._get_token()
        headers = dict(self._default_headers)
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

        if method == "PATCH":
            headers["Content-Type"] = content_type or "application/json-patch+json"
        elif content_type is not None:
            headers["Content-Type"] = content_type

        data_str: Optional[str] = None
        if body is not None and method in ("POST", "PUT", "PATCH", "DELETE"):
            data_str = json.dumps(body)

        try:
            resp = self._session.request(
                method=method,
                url=url,
                headers=headers,
                data=data_str,
                timeout=self._timeout,
                verify=self._verify,
            )
        except Exception as exc:
            msg = str(exc)
            return SSResponse(
                0,
                {"resourceType": "OperationOutcome", "issue": [{"details": {"text": msg}}]},
                msg,
            )

        if resp.status_code >= 400:
            return self._handle_failure(method, url, resp, body, content_type)

        return self._build_response(resp)

    def _handle_failure(
        self,
        method: str,
        url: str,
        response: requests.Response,
        body: Optional[Union[dict[str, Any], list[Any]]] = None,
        content_type: Optional[str] = None,
    ) -> SSResponse:
        status_code = int(response.status_code)
        content = response.text or ""
        try:
            body_dict = response.json()
            if not isinstance(body_dict, dict):
                body_dict = {}
        except ValueError:
            body_dict = {}

        # 429 — rate limited: read Retry-After header
        if status_code == 429:
            self._retry_count += 1
            if self._retry_count > self._max_retries:
                return SSResponse(status_code, body_dict, content)

            retry_after = ""
            if hasattr(response, "headers") and response.headers:
                retry_after = response.headers.get("Retry-After", "") or response.headers.get("retry-after", "")
            try:
                sleep_sec = int(retry_after) if retry_after != "" else (2 ** self._retry_count)
            except ValueError:
                sleep_sec = 2 ** self._retry_count

            self._sleep(sleep_sec)
            return self._do_request(method, url, body, content_type)

        # 401 — unauthorized: attempt token refresh
        if status_code == 401:
            if self._should_auto_refresh() and self._oauth2 is not None:
                self._retry_count += 1
                if self._retry_count > self._max_retries:
                    return SSResponse(status_code, body_dict, content)

                refresh_fn = getattr(self._oauth2, "refresh_token", None) or getattr(
                    self._oauth2, "refreshToken", None
                )
                if callable(refresh_fn):
                    refresh_fn()
                self._token = None

                self._sleep(2 ** self._retry_count)
                return self._do_request(method, url, body, content_type)

            return SSResponse(status_code, body_dict, content)

        # 5xx — server error: exponential backoff
        if status_code >= 500:
            self._retry_count += 1
            if self._retry_count > self._max_retries:
                return SSResponse(status_code, body_dict, content)

            self._sleep(2 ** self._retry_count)
            return self._do_request(method, url, body, content_type)

        return SSResponse(status_code, body_dict, content)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _build_url(self, url: str, params: Optional[dict[str, Any]] = None) -> str:
        if url.startswith("http://") or url.startswith("https://"):
            full = url
        else:
            full = f"{self._base_url}/{url.lstrip('/')}" if self._base_url else url.lstrip("/")

        if not params:
            return full

        sep = "&" if "?" in full else "?"
        return f"{full}{sep}{urlencode(params, doseq=True)}"

    def _build_response(self, response: requests.Response) -> SSResponse:
        status_code = int(response.status_code)
        content = response.text or ""
        try:
            body_dict = response.json()
            if not isinstance(body_dict, dict):
                body_dict = {}
        except ValueError:
            body_dict = {}

        return SSResponse(status_code, body_dict, content)

    def _sleep(self, seconds: int) -> None:
        if seconds <= 0:
            return
        capped = min(seconds, 60)
        self._sleep_fn(capped)
