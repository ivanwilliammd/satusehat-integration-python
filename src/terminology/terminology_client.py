"""TerminologyClient — standalone HTTP client untuk SmarTerm (terminology.ivanmd.id).

TERPISAH dari ekosistem SATUSEHAT: jangan reuse OAuth SATUSEHAT Kemkes.
SmarTerm punya auth sendiri, dual-mode:

  1. Sanctum Personal Access Token (PAT) — token statis, header ``Bearer``.
     Env: TERMINOLOGY_API_TOKEN (atau argumen ``token``).
  2. OIDC client_credentials ke auth.ivanmd.id (Passport) — client fetch JWT
     sendiri, cache sampai expire, auto-refresh saat 401.
     Env: TERMINOLOGY_CLIENT_ID / TERMINOLOGY_CLIENT_SECRET /
          TERMINOLOGY_TOKEN_URL (default https://auth.ivanmd.id/oauth/token)

Jika keduanya diberikan, PAT menang (lebih sederhana). OIDC dipakai saat
``token`` kosong dan kredensial client tersedia.

Fluent chaining:
  client.query('pemasangan kateter').on('kptl').limit(10).get()
  client.query('paracetamol').all().first()
"""
from __future__ import annotations

import os
import time
from typing import Any, Optional
from urllib.parse import quote

import requests

from .terminology_query_builder import TerminologyQueryBuilder

DEFAULT_BASE_URL = "https://terminology.ivanmd.id"
DEFAULT_TOKEN_URL = "https://auth.ivanmd.id/oauth/token"


class TerminologyClient:
    """HTTP client mirror PHP Satusehat\\Integration\\TerminologyClient."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token_url: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        self.base_url = (base_url or os.getenv("TERMINOLOGY_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.token = token or os.getenv("TERMINOLOGY_API_TOKEN")
        self.client_id = client_id or os.getenv("TERMINOLOGY_CLIENT_ID") or ""
        self.client_secret = client_secret or os.getenv("TERMINOLOGY_CLIENT_SECRET") or ""
        self.token_url = token_url or os.getenv("TERMINOLOGY_TOKEN_URL") or DEFAULT_TOKEN_URL
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "satusehat-integration/terminology-client",
            }
        )

        # OIDC cached token.
        self._oidc_token: Optional[str] = None
        self._oidc_expires_at: int = 0

    # ─── Entry & raw HTTP ────────────────────────────────────────────────────

    def query(self, text: str) -> TerminologyQueryBuilder:
        """Fluent query builder — entry: query('istilah')->on('kfa')->limit(5)->get()."""
        return TerminologyQueryBuilder(self, text)

    def request(
        self,
        method: str,
        path: str,
        query: Optional[dict] = None,
        body: Optional[dict] = None,
    ) -> tuple[int, Any]:
        """Raw HTTP helper — auto auth header; OIDC refresh-once on 401.

        Returns (status, decoded_body). Error HTTP >= 400 dilempar oleh wrapper
        method publik (``search``, ``validate``, dll), bukan di sini.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        params = query or None
        headers = {}
        token = self._resolve_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            res = self.session.request(method, url, params=params, json=body, headers=headers, timeout=self.timeout)
        except requests.RequestException as e:
            raise RuntimeError(f"TerminologyClient network error: {e}") from e

        # OIDC mode: token expire → refresh sekali lalu retry.
        if res.status_code == 401 and not self.token and self.client_id:
            self._oidc_token = None
            self._oidc_expires_at = 0
            token = self._fetch_oidc_token()
            if token:
                headers["Authorization"] = f"Bearer {token}"
                res = self.session.request(method, url, params=params, json=body, headers=headers, timeout=self.timeout)

        try:
            decoded = res.json()
        except ValueError:
            decoded = {"raw": res.text}

        return res.status_code, decoded

    # ─── Unified & per-system search ─────────────────────────────────────────

    def search(self, query: str, category: str = "all", limit: int = 20) -> Any:
        """GET /api/v1/terminology/search?q=&category=&limit="""
        status, body = self.request(
            "GET",
            "api/v1/terminology/search",
            {"q": query, "category": category, "limit": self._clamp_limit(limit)},
        )
        return self._unwrap(status, body)

    def search_system(self, system: str, query: str, limit: int = 20) -> Any:
        """GET /api/v1/terminology/{system}/search — system: icd10|icd9cm|snomed|loinc|kfa|kfa_alkes|kfa_bza|kptl"""
        status, body = self.request(
            "GET",
            f"api/v1/terminology/{quote(system)}/search",
            {"q": query, "limit": self._clamp_limit(limit)},
        )
        return self._unwrap(status, body)

    def kptl_combine(self, base_code: str, modifiers: Optional[list] = None) -> Any:
        """GET /api/v1/terminology/kptl/combine?base_code=&modifiers= — multi-layer KPTL."""
        status, body = self.request(
            "GET",
            "api/v1/terminology/kptl/combine",
            {"base_code": base_code, "modifiers": ",".join(modifiers or [])},
        )
        return self._unwrap(status, body)

    def map(self, source: str, target: str, code: str) -> Any:
        """GET /api/v1/terminology/mapping?source=&target=&code= — cross-terminology mapping."""
        status, body = self.request(
            "GET",
            "api/v1/terminology/mapping",
            {"source": source, "target": target, "code": code},
        )
        return self._unwrap(status, body)

    def validate(self, system: str, code: str) -> Any:
        """POST /api/v1/terminology/validate — { system, code }."""
        status, body = self.request("POST", "api/v1/terminology/validate", None, {"system": system, "code": code})
        return self._unwrap(status, body)

    def auto_map(self, source_system: str, source_code: str) -> Any:
        """POST /api/v1/terminology/auto-map — { source_system, source_code } → SNOMED."""
        status, body = self.request(
            "POST", "api/v1/terminology/auto-map", None, {"source_system": source_system, "source_code": source_code}
        )
        return self._unwrap(status, body)

    # ─── Context-aware FHIR resolution ───────────────────────────────────────

    def resolve_condition(
        self, code: str, system_hint: Optional[str] = None, category: str = "encounter-diagnosis"
    ) -> Any:
        return self._resolve("condition", {"code": code, "system_hint": system_hint, "category": category})

    def resolve_chief_complaint(self, code: str) -> Any:
        return self._resolve("chief-complaint", {"code": code})

    def resolve_observation(self, code: str, system_hint: Optional[str] = None) -> Any:
        return self._resolve("observation", {"code": code, "system_hint": system_hint})

    def resolve_medication(self, code: str) -> Any:
        return self._resolve("medication", {"code": code})

    def resolve_service_request(self, code: str, category: str = "lab") -> Any:
        return self._resolve("service-request", {"code": code, "category": category})

    # ─── Value sets ──────────────────────────────────────────────────────────

    def value_sets(self) -> Any:
        """GET /api/value-sets."""
        status, body = self.request("GET", "api/value-sets")
        return self._unwrap(status, body)

    def value_set(self, bundle_id: str) -> Any:
        """GET /api/value-sets/{bundleId}."""
        status, body = self.request("GET", f"api/value-sets/{quote(bundle_id)}")
        return self._unwrap(status, body)

    # ─── Internals ───────────────────────────────────────────────────────────

    def _resolve_token(self) -> Optional[str]:
        """Static PAT menang; kalau kosong dan ada OIDC creds → lazy fetch + cache."""
        if self.token:
            return self.token
        if not self.client_id:
            return None
        if self._oidc_token and time.time() < self._oidc_expires_at - 30:
            return self._oidc_token
        if self._oidc_token is None:
            self._oidc_token = self._fetch_oidc_token()
        return self._oidc_token

    def _fetch_oidc_token(self) -> Optional[str]:
        """POST {token_url} grant_type=client_credentials → access_token."""
        try:
            res = self.session.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                timeout=self.timeout,
            )
        except requests.RequestException:
            return None
        if res.status_code >= 400:
            return None
        data = res.json()
        access_token = data.get("access_token")
        if not isinstance(access_token, str) or not access_token:
            return None
        self._oidc_token = access_token
        self._oidc_expires_at = int(time.time() + data.get("expires_in", 3600))
        return access_token

    def _resolve(self, kind: str, payload: dict) -> Any:
        body = {k: v for k, v in payload.items() if v is not None}
        status, data = self.request("POST", f"api/v1/terminology/resolve/{kind}", None, body)
        return self._unwrap(status, data)

    @staticmethod
    def _clamp_limit(limit: int) -> int:
        return max(1, min(limit, 100))

    def _unwrap(self, status: int, body: Any) -> Any:
        """Lempar RuntimeError kalau HTTP >= 400; else return envelope penuh."""
        if status >= 400:
            if isinstance(body, dict):
                detail = body.get("message") or body.get("error")
            else:
                detail = None
            raise RuntimeError(f"TerminologyClient HTTP {status}: {detail if detail is not None else body}")
        return body
