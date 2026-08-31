"""
SNOMED CT terminology model.

Ported from: Satusehat\Integration\Terminology\Snomedct
Source: satusehat-integration (Laravel)

@property str code
@property str fsn
@property str preferred
@property str acceptable
@property str version
@property str hierarchy
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class Snomedct(TerminologyBase):
    """
    SNOMED Clinical Terms (CT) terminology.

    Ported from Laravel Eloquent model Snomedct.
    Table: satusehat_snomedct.
    """

    table_name: str = "satusehat_snomedct"
    columns: list[str] = [
        "id",
        "code",
        "fsn",
        "preferred",
        "acceptable",
        "version",
        "hierarchy",
        "created_at",
        "updated_at",
        "deleted_at",
    ]
    primary_key: str = "id"
    code_column: str = "code"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the satusehat_snomedct table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS satusehat_snomedct (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                fsn TEXT NOT NULL,
                preferred TEXT,
                acceptable TEXT,
                version TEXT,
                hierarchy TEXT,
                created_at TEXT,
                updated_at TEXT,
                deleted_at TEXT
            )
        """)
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_snomedct_code ON satusehat_snomedct(code)")
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[Snomedct]:
        """Find SNOMED CT entry by code."""
        return super().find_by_code(code)  # type: ignore[return-value]
