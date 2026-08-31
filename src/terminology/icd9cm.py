"""
ICD-9-CM terminology model.

Ported from: Satusehat\Integration\Terminology\Icd9cm
Source: satusehat-integration (Laravel)

@property str icd9cm_code
@property str icd9cm_en
@property str icd9cm_id
@property bool active
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class Icd9cm(TerminologyBase):
    """
    ICD-9-CM classification codes for procedures.

    Ported from Laravel Eloquent model Icd9cm.
    Table: satusehat_icd9cm (configurable via config()).
    """

    table_name: str = "satusehat_icd9cm"
    columns: list[str] = [
        "id",
        "icd9cm_code",
        "icd9cm_en",
        "icd9cm_id",
        "active",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "icd9cm_code"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the satusehat_icd9cm table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS satusehat_icd9cm (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                icd9cm_code TEXT NOT NULL,
                icd9cm_en TEXT NOT NULL,
                icd9cm_id TEXT,
                active INTEGER DEFAULT 1,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_icd9cm_code ON satusehat_icd9cm(icd9cm_code)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_icd9cm_id ON satusehat_icd9cm(icd9cm_id)")
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[Icd9cm]:
        """Find ICD-9-CM entry by code."""
        return super().find_by_code(code)  # type: ignore[return-value]

    @classmethod
    def find_by_icd9cm_id(cls, icd9cm_id: str) -> Optional[Icd9cm]:
        """Find ICD-9-CM entry by Indonesian ICD-9-CM ID."""
        conn = cls.get_connection()
        row = conn.execute(
            "SELECT * FROM satusehat_icd9cm WHERE icd9cm_id = ?", (icd9cm_id,)
        ).fetchone()
        return cls._row_to_instance(row) if row else None  # type: ignore[return-value]
