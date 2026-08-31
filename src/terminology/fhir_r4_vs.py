"""
FHIR R4 ValueSet terminology model.

Ported from: Satusehat\Integration\Terminology\FhirR4vs
Source: satusehat-integration (Laravel)

@property str fhir_id
@property str url
@property str version
@property str name
@property str title
@property str status
@property bool experimental
@property str description
@property str date
@property str publisher
@property str content
@property str concept_code_l1
@property str concept_display_l1
@property str concept_definition_l1
@property str concept_code_l2
@property str concept_display_l2
@property str concept_definition_l2
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class FhirR4vs(TerminologyBase):
    """
    FHIR R4 ValueSet terminology entries.

    Ported from Laravel Eloquent model FhirR4vs.
    Table: fhir_r4_vs.
    """

    table_name: str = "fhir_r4_vs"
    columns: list[str] = [
        "id",
        "fhir_id",
        "url",
        "version",
        "name",
        "title",
        "status",
        "experimental",
        "description",
        "date",
        "publisher",
        "content",
        "concept_code_l1",
        "concept_display_l1",
        "concept_definition_l1",
        "concept_code_l2",
        "concept_display_l2",
        "concept_definition_l2",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "fhir_id"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the fhir_r4_vs table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fhir_r4_vs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fhir_id TEXT NOT NULL,
                url TEXT NOT NULL,
                version TEXT NOT NULL,
                name TEXT NOT NULL,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                experimental INTEGER DEFAULT 0,
                description TEXT NOT NULL,
                date TEXT,
                publisher TEXT NOT NULL,
                content TEXT NOT NULL,
                concept_code_l1 TEXT,
                concept_display_l1 TEXT,
                concept_definition_l1 TEXT,
                concept_code_l2 TEXT,
                concept_display_l2 TEXT,
                concept_definition_l2 TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[FhirR4vs]:
        """Find FhirR4vs entry by fhir_id."""
        return super().find_by_code(code)  # type: ignore[return-value]

    @classmethod
    def find_by_url(cls, url: str) -> list[FhirR4vs]:
        """Find all entries for a given ValueSet URL."""
        conn = cls.get_connection()
        rows = conn.execute(
            "SELECT * FROM fhir_r4_vs WHERE url = ?", (url,)
        ).fetchall()
        return [cls._row_to_instance(r) for r in rows]  # type: ignore[return-value]
