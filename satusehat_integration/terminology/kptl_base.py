r"""
KPTL Base terminology model.

Ported from: Satusehat\Integration\Terminology\KptlBase
Source: satusehat-integration (Laravel)

@property str status
@property str base_code
@property str base_display
@property str modifier_1
@property str modifier_2
@property str modifier_3
@property str modifier_4
@property str modifier_5
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class KptlBase(TerminologyBase):
    """
    KPTL (Kode Pelaporan Tindakan Layanan) base procedure codes.

    Ported from Laravel Eloquent model KptlBase.
    Table: kptl_base.
    """

    table_name: str = "kptl_base"
    columns: list[str] = [
        "id",
        "status",
        "base_code",
        "base_display",
        "modifier_1",
        "modifier_2",
        "modifier_3",
        "modifier_4",
        "modifier_5",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "base_code"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the kptl_base table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS kptl_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL,
                base_code TEXT NOT NULL,
                base_display TEXT NOT NULL,
                modifier_1 TEXT,
                modifier_2 TEXT,
                modifier_3 TEXT,
                modifier_4 TEXT,
                modifier_5 TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[KptlBase]:
        """Find KptlBase entry by base_code."""
        return super().find_by_code(code)  # type: ignore[return-value]
