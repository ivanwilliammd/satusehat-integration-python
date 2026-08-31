"""
ICD-10 terminology model.

Ported from: Satusehat\Integration\Terminology\Icd10
Source: satusehat-integration (Laravel)

@property str icd10_code
@property str icd10_en
@property str icd10_id
@property bool active
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class Icd10(TerminologyBase):
    """
    ICD-10 classification codes for diagnoses.

    Ported from Laravel Eloquent model Icd10.
    Table: satusehat_icd10 (configurable via config()).
    """

    table_name: str = "satusehat_icd10"
    columns: list[str] = [
        "id",
        "icd10_code",
        "icd10_en",
        "icd10_id",
        "active",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "icd10_code"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the satusehat_icd10 table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS satusehat_icd10 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                icd10_code TEXT NOT NULL,
                icd10_en TEXT NOT NULL,
                icd10_id TEXT,
                active INTEGER DEFAULT 1,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_icd10_code ON satusehat_icd10(icd10_code)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_icd10_id ON satusehat_icd10(icd10_id)")
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[Icd10]:
        """Find ICD-10 entry by code."""
        return super().find_by_code(code)  # type: ignore[return-value]

    @classmethod
    def find_by_icd10_id(cls, icd10_id: str) -> Optional[Icd10]:
        """Find ICD-10 entry by Indonesian ICD-10 ID."""
        conn = cls.get_connection()
        row = conn.execute(
            "SELECT * FROM satusehat_icd10 WHERE icd10_id = ?", (icd10_id,)
        ).fetchone()
        return cls._row_to_instance(row) if row else None  # type: ignore[return-value]
