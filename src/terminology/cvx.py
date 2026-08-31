"""
CVX (Vaccine Administered) terminology model.

Ported from: Satusehat\Integration\Terminology\Cvx
Source: satusehat-integration (Laravel)

@property str cvx_code
@property str cvx_short_description
@property str full_vaccine_name
@property str note
@property str vaccine_status
@property int internal_id
@property bool nonvaccine
@property str update_date
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class Cvx(TerminologyBase):
    """
    CVX (Vaccine Administered) terminology codes.

    Ported from Laravel Eloquent model Cvx.
    Table: satusehat_cvx.
    """

    table_name: str = "satusehat_cvx"
    columns: list[str] = [
        "id",
        "cvx_code",
        "cvx_short_description",
        "full_vaccine_name",
        "note",
        "vaccine_status",
        "internal_id",
        "nonvaccine",
        "update_date",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "cvx_code"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the satusehat_cvx table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS satusehat_cvx (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cvx_code TEXT NOT NULL,
                cvx_short_description TEXT NOT NULL,
                full_vaccine_name TEXT NOT NULL,
                note TEXT,
                vaccine_status TEXT NOT NULL,
                internal_id INTEGER NOT NULL,
                nonvaccine INTEGER DEFAULT 0,
                update_date TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[Cvx]:
        """Find CVX entry by cvx_code."""
        return super().find_by_code(code)  # type: ignore[return-value]
