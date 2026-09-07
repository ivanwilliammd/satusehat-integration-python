"""TerminologyQueryBuilder — fluent query builder untuk SmarTerm.

  client.query('pemasangan kateter').on('kptl').limit(10).get()
  client.query('demam').category('diagnosis').first()
  client.query('paracetamol').on('kfa').all()
  client.query('93004944').as_code().get()   # validate
"""
from __future__ import annotations

import re
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .terminology_client import TerminologyClient


class TerminologyQueryBuilder:
    """Fluent builder mirror PHP Satusehat\\Integration\\TerminologyQueryBuilder."""

    def __init__(self, client: "TerminologyClient", text: str) -> None:
        self._client = client
        self._text = text
        # None = unified search (/search); str = per-system.
        self._system: Optional[str] = None
        self._category: str = "all"
        self._limit: int = 20
        self._as_code: bool = False

    def on(self, system: str) -> "TerminologyQueryBuilder":
        """Scope ke satu sistem: icd10|icd9cm|snomed|loinc|kfa|kfa_alkes|kfa_bza|kptl."""
        self._system = system
        return self

    def category(self, category: str) -> "TerminologyQueryBuilder":
        """Unified search category: all|diagnosis|procedure|medication|lab|imaging|..."""
        self._category = category
        return self

    def limit(self, limit: int) -> "TerminologyQueryBuilder":
        """Clamp 1-100."""
        self._limit = max(1, min(limit, 100))
        return self

    def as_code(self) -> "TerminologyQueryBuilder":
        """Treat text as exact code → validate (POST /validate)."""
        self._as_code = True
        return self

    def first(self) -> "TerminologyQueryBuilder":
        """Alias limit(1)."""
        return self.limit(1)

    def all(self) -> "TerminologyQueryBuilder":
        """Max 100 hasil."""
        return self.limit(100)

    def get(self) -> object:
        """Execute — search (GET) atau validate (POST). Returns envelope."""
        if self._as_code:
            # text = code; butuh system tujuan utk validate. Kalau belum di-scope,
            # coba tebak sistem dari bentuk kode.
            system = self._system or self._guess_system_from_code(self._text)
            return self._client.validate(system, self._text)

        if self._system is not None:
            return self._client.search_system(self._system, self._text, self._limit)

        return self._client.search(self._text, self._category, self._limit)

    @staticmethod
    def _guess_system_from_code(code: str) -> str:
        if code.isdigit() and code.startswith("93"):
            return "kfa"
        if code.isdigit() and code.startswith("83"):
            return "kfa_alkes"
        if code.isdigit() and code.startswith("91"):
            return "kfa_bza"
        if code.isdigit() and 5 <= len(code) <= 7:
            return "snomed"
        if code.isdigit() or (code.replace(".", "", 1).isdigit() and code.count(".") == 1):
            return "icd9cm"
        if re.fullmatch(r"[A-Z]\d{2}(\.\d+)?", code):
            return "icd10"
        if "-" in code:
            return "loinc"
        return "snomed"
