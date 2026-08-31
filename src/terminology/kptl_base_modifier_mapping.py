r"""
KPTL Base Modifier Mapping terminology model.

Ported from: Satusehat\Integration\Terminology\KptlBaseModifierMapping
Source: satusehat-integration (Laravel)

@property str display
@property str modifier_1
@property str modifier_2
@property str modifier_3
@property str modifier_4
@property str modifier_5
@property str base_code
@property str modifier_code_1
@property str modifier_code_2
@property str modifier_code_3
@property str modifier_code_4
@property str modifier_code_5
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class KptlBaseModifierMapping(TerminologyBase):
    """
    KPTL Base to Modifier mapping for complete procedure codes.

    Ported from Laravel Eloquent model KptlBaseModifierMapping.
    Table: kptl_base_modifier_mapping.
    """

    table_name: str = "kptl_base_modifier_mapping"
    columns: list[str] = [
        "id",
        "display",
        "modifier_1",
        "modifier_2",
        "modifier_3",
        "modifier_4",
        "modifier_5",
        "base_code",
        "modifier_code_1",
        "modifier_code_2",
        "modifier_code_3",
        "modifier_code_4",
        "modifier_code_5",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "base_code"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the kptl_base_modifier_mapping table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS kptl_base_modifier_mapping (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display TEXT NOT NULL,
                modifier_1 TEXT,
                modifier_2 TEXT,
                modifier_3 TEXT,
                modifier_4 TEXT,
                modifier_5 TEXT,
                base_code TEXT NOT NULL,
                modifier_code_1 TEXT,
                modifier_code_2 TEXT,
                modifier_code_3 TEXT,
                modifier_code_4 TEXT,
                modifier_code_5 TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[KptlBaseModifierMapping]:
        """Find mapping by base_code."""
        return super().find_by_code(code)  # type: ignore[return-value]
