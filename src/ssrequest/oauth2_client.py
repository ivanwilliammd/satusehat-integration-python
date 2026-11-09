"""OAuth2Client — SATUSEHAT OAuth2 authentication and legacy request helpers."""
from __future__ import annotations

import json
import os
import time
from typing import Any, Callable, Optional, Union
from urllib.parse import urlparse

import requests


class OAuth2ClientException(ValueError):
    """Raised when SATUSEHAT OAuth2 environment or credentials are misconfigured."""


class OAuth2Client:
    """SATUSEHAT OAuth2 Client supporting DEV, STG, and PROD environments."""

    ENV_BASE_URLS = {
        "DEV": "https://api-satusehat-dev.dto.kemkes.go.id",
        "STG": "https://api-satusehat-stg.dto.kemkes.go.id",
        "PROD": "https://api-satusehat.kemkes.go.id",
    }

    def __init__(
        self,
        satusehat_env: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        organization_id: Optional[str] = None,
        base_url: Optional[str] = None,
        override: bool = False,
        auto_refresh: bool = True,
        session: Optional[requests.Session] = None,
        logger: Optional[Callable[..., None]] = None,
    ) -> None:
        self.patient_dev = [
            "P02478375538",
            "P02428473601",
            "P03647103112",
            "P01058967035",
            "P01836748436",
            "P01654557057",
            "P00805884304",
            "P00883356749",
            "P00912894463",
        ]
        self.practitioner_dev = [
            "10009880728",
            "10006926841",
            "10001354453",
            "10010910332",
            "10018180913",
            "10002074224",
            "10012572188",
            "10018452434",
            "10014058550",
            "10001915884",
        ]

        self.override = override
        self._auto_refresh = auto_refresh
        self.session = session or requests.Session()
        self._logger = logger
        self.logs: list[dict[str, Any]] = []

        self._cached_token: Optional[str] = None
        self._token_created_at: float = 0.0
        self._token_ttl_seconds: float = 50 * 60  # 50 minutes

        self.oauth2_error = {
            "statusCode": 401,
            "res": "Unauthorized. Token not found",
        }

        self.satusehat_env: Optional[str] = None if self.override else (satusehat_env or os.getenv("SATUSEHAT_ENV"))
        self.base_url: Optional[str] = None
        self.client_id: Optional[str] = client_id
        self.client_secret: Optional[str] = client_secret
        self.organization_id: Optional[str] = organization_id

        if self.satusehat_env == "PROD":
            self.base_url = base_url or os.getenv("SATUSEHAT_BASE_URL_PROD") or self.ENV_BASE_URLS["PROD"]
            self.client_id = self.client_id or os.getenv("CLIENTID_PROD")
            self.client_secret = self.client_secret or os.getenv("CLIENTSECRET_PROD")
            self.organization_id = self.organization_id or os.getenv("ORGID_PROD")
        elif self.satusehat_env == "STG":
            self.base_url = base_url or os.getenv("SATUSEHAT_BASE_URL_STG") or self.ENV_BASE_URLS["STG"]
            self.client_id = self.client_id or os.getenv("CLIENTID_STG")
            self.client_secret = self.client_secret or os.getenv("CLIENTSECRET_STG")
            self.organization_id = self.organization_id or os.getenv("ORGID_STG")
        elif self.satusehat_env == "DEV":
            self.base_url = base_url or os.getenv("SATUSEHAT_BASE_URL_DEV") or self.ENV_BASE_URLS["DEV"]
            self.client_id = self.client_id or os.getenv("CLIENTID_DEV")
            self.client_secret = self.client_secret or os.getenv("CLIENTSECRET_DEV")
            self.organization_id = self.organization_id or os.getenv("ORGID_DEV")

        if not self.satusehat_env and not self.override:
            raise OAuth2ClientException("SATUSEHAT environment is missing")

        if self.satusehat_env not in ("DEV", "STG", "PROD") and not self.override:
            raise OAuth2ClientException(
                f"SATUSEHAT environment invalid, supported (DEV, STG, PROD). {self.satusehat_env} given."
            )

        if self.satusehat_env in ("DEV", "STG", "PROD") and not self.override:
            if not self.client_id or not self.client_secret or not self.organization_id:
                env = self.satusehat_env
                raise OAuth2ClientException(
                    f"SATUSEHAT environment defined as {env}, but CLIENTID_{env} / CLIENTSECRET_{env} / ORGID_{env} not set"
                )

        if self.override:
            self.base_url = base_url

        auth_endpoint = os.getenv("SATUSEHAT_AUTH_ENDPOINT") or "/oauth2/v1"
        fhir_endpoint = os.getenv("SATUSEHAT_FHIR_ENDPOINT") or "/fhir-r4/v1"

        base = self.base_url or ""
        self.auth_url = f"{base}{auth_endpoint}"
        self.fhir_url = f"{base}{fhir_endpoint}"

    def is_token_auto_refresh(self) -> bool:
        return self._auto_refresh

    isTokenAutoRefresh = is_token_auto_refresh

    def refresh_token(self) -> Any:
        """Force token invalidation and fetch a fresh OAuth2 access token."""
        self._cached_token = None
        self._token_created_at = 0.0
        return self.token()

    refreshToken = refresh_token

    def token(self) -> Any:
        """Retrieve a valid SATUSEHAT access token (from 50-minute cache or OAuth2 endpoint)."""
        now = time.time()
        if self._cached_token and (now - self._token_created_at) < self._token_ttl_seconds:
            return self._cached_token

        url = f"{self.auth_url}/accesstoken?grant_type=client_credentials"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        try:
            res = self.session.post(url, data=data, headers=headers, timeout=30)
            try:
                contents = res.json()
            except ValueError:
                contents = {}

            if res.status_code >= 400:
                issue_info = None
                if isinstance(contents, dict):
                    issues = contents.get("issue")
                    if isinstance(issues, list) and issues and isinstance(issues[0], dict):
                        details = issues[0].get("details")
                        if isinstance(details, dict):
                            issue_info = details.get("text")
                issue_info = issue_info or f"HTTP {res.status_code}"
                self.log(issue_info, "POST Token", url, None, contents if isinstance(contents, dict) else {})
                return issue_info

            if isinstance(contents, dict) and contents.get("access_token"):
                self._cached_token = str(contents["access_token"])
                self._token_created_at = now
                return self._cached_token

            return self.respond_error(self.oauth2_error)
        except requests.RequestException as exc:
            self.log(str(exc), "POST Token", url, None, {"error": str(exc)})
            return str(exc)

    def log(
        self,
        response_id: Any,
        action: str,
        url: str,
        payload: Optional[dict[str, Any]],
        response: Any,
    ) -> None:
        entry = {
            "response_id": response_id,
            "action": action,
            "url": url,
            "payload": payload,
            "response": response,
        }
        self.logs.append(entry)
        if self._logger:
            self._logger(entry)

    def respond_error(self, message: dict[str, Any]) -> list[Any]:
        return [message["statusCode"], message["res"]]

    respondError = respond_error

    def get_by_id(self, resource: str, resource_id: str) -> list[Any]:
        access_token = self.token()
        if not isinstance(access_token, str) or isinstance(access_token, list):
            return self.respond_error(self.oauth2_error)

        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{self.fhir_url}/{resource}/{resource_id}"

        try:
            res = self.session.get(url, headers=headers, timeout=30)
            status_code = res.status_code
            try:
                response = res.json()
            except ValueError:
                response = {}

            if status_code >= 400:
                self.log(f"Error {status_code}", "GET", url, None, response)
                return [status_code, response]

            log_id = resource_id
            if isinstance(response, dict) and (
                response.get("resourceType") == "OperationOutcome" or response.get("total") == 0
            ):
                log_id = f"Error {status_code}"
            self.log(log_id, "GET", url, None, response)
            return [status_code, response]
        except requests.RequestException as exc:
            self.log("Error 0", "GET", url, None, {"error": str(exc)})
            return [0, {"error": str(exc)}]

    getById = get_by_id

    def get_by_nik(self, resource: str, nik: str) -> list[Any]:
        access_token = self.token()
        if not isinstance(access_token, str) or isinstance(access_token, list):
            return self.respond_error(self.oauth2_error)

        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{self.fhir_url}/{resource}?identifier=https://fhir.kemkes.go.id/id/nik|{nik}"

        try:
            res = self.session.get(url, headers=headers, timeout=30)
            status_code = res.status_code
            try:
                response = res.json()
            except ValueError:
                response = {}

            if status_code >= 400:
                self.log(f"Error {status_code}", "GET", url, None, response)
                return [status_code, response]

            if isinstance(response, dict) and (
                response.get("resourceType") == "OperationOutcome" or response.get("total") == 0
            ):
                log_id = "Not Found"
            else:
                entries = response.get("entry") if isinstance(response, dict) else None
                if isinstance(entries, list) and entries and isinstance(entries[0], dict):
                    log_id = (entries[0].get("resource") or {}).get("id", "Not Found")
                else:
                    log_id = "Not Found"

            self.log(log_id, "GET", url, None, response)
            return [status_code, response]
        except requests.RequestException as exc:
            self.log("Error 0", "GET", url, None, {"error": str(exc)})
            return [0, {"error": str(exc)}]

    getByNik = get_by_nik

    def ss_kfa_get(self, resource: str, query_string: str) -> list[Any]:
        access_token = self.token()
        if not isinstance(access_token, str) or isinstance(access_token, list):
            return self.respond_error(self.oauth2_error)

        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{self.base_url}/kfa-v2/{resource}{query_string}"

        try:
            res = self.session.get(url, headers=headers, timeout=30)
            status_code = res.status_code
            try:
                response = res.json()
            except ValueError:
                response = {}

            if status_code >= 400:
                self.log(f"Error {status_code}", "GET", url, None, response)
                return [status_code, response]

            log_id = f"Kfa_GET_{resource}"
            if resource == "products/all?" and isinstance(response, dict) and not response.get("total"):
                log_id = "Not Found"
            elif resource == "products?" and isinstance(response, dict) and not response.get("result"):
                log_id = "Not Found"

            self.log(log_id, "GET", url, None, response)
            return [status_code, response]
        except requests.RequestException as exc:
            self.log("Error 0", "GET", url, None, {"error": str(exc)})
            return [0, {"error": str(exc)}]

    ssKfaGet = ss_kfa_get

    def ss_post(self, resource: str, body: Union[str, dict[str, Any]]) -> list[Any]:
        access_token = self.token()
        if not isinstance(access_token, str) or isinstance(access_token, list):
            return self.respond_error(self.oauth2_error)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        url = self.fhir_url if resource == "Bundle" else f"{self.fhir_url}/{resource}"
        body_str = json.dumps(body) if isinstance(body, dict) else str(body)
        body_dict = body if isinstance(body, dict) else (json.loads(body_str) if body_str else {})

        try:
            res = self.session.post(url, data=body_str, headers=headers, timeout=30)
            status_code = res.status_code
            try:
                response = res.json()
            except ValueError:
                response = {}

            if status_code >= 400:
                self.log(f"Error {status_code}", "POST", url, body_dict, response)
                return [status_code, response]

            log_id = f"Success {status_code}"
            if resource == "Patient" and isinstance(body_dict, dict):
                identifiers = body_dict.get("identifier") or []
                sys_url = identifiers[0].get("system", "") if identifiers and isinstance(identifiers[0], dict) else ""
                parsed_path = urlparse(sys_url).path
                parts = parsed_path.split("/")
                identifier_type = parts[2] if len(parts) > 2 else ""
                if identifier_type == "nik" and isinstance(response, dict):
                    log_id = (response.get("data") or {}).get("patient_id") or f"Error {status_code}"
                elif identifier_type == "nik-ibu" and isinstance(response, dict):
                    cp = response.get("create_patient") or {}
                    log_id = (cp.get("data") or {}).get("patient_id") or f"Error {status_code}"
            elif isinstance(response, dict):
                if response.get("resourceType") == "OperationOutcome":
                    log_id = f"Error {status_code}"
                elif resource != "Bundle":
                    log_id = response.get("id") or log_id

            self.log(log_id, "POST", url, body_dict, response)
            return [status_code, response]
        except requests.RequestException as exc:
            self.log("Error 0", "POST", url, body_dict, {"error": str(exc)})
            return [0, {"error": str(exc)}]

    ssPost = ss_post

    def ss_put(self, resource: str, resource_id: str, body: Union[str, dict[str, Any]]) -> list[Any]:
        access_token = self.token()
        if not isinstance(access_token, str) or isinstance(access_token, list):
            return self.respond_error(self.oauth2_error)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        url = f"{self.fhir_url}/{resource}/{resource_id}"
        body_str = json.dumps(body) if isinstance(body, dict) else str(body)
        body_dict = body if isinstance(body, dict) else (json.loads(body_str) if body_str else {})

        try:
            res = self.session.put(url, data=body_str, headers=headers, timeout=30)
            status_code = res.status_code
            try:
                response = res.json()
            except ValueError:
                response = {}

            if status_code >= 400 or (isinstance(response, dict) and response.get("resourceType") == "OperationOutcome"):
                log_id = f"Error {status_code}"
            else:
                log_id = response.get("id", resource_id) if isinstance(response, dict) else resource_id

            self.log(log_id, "PUT", url, body_dict, response)
            return [status_code, response]
        except requests.RequestException as exc:
            self.log("Error 0", "PUT", url, body_dict, {"error": str(exc)})
            return [0, {"error": str(exc)}]

    ssPut = ss_put
