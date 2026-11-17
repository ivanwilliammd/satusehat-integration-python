r"""
KPTL Modifier terminology model.

Ported from: Satusehat\Integration\Terminology\KptlModifier
Source: satusehat-integration (Laravel)

@property str kategori_kelompok
@property str item
@property str modifier_code
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class KptlModifier(TerminologyBase):
    """
    KPTL Modifier codes for procedure variations.

    Ported from Laravel Eloquent model KptlModifier.
    Table: kptl_modifier.
    """

    table_name: str = "kptl_modifier"
    columns: list[str] = [
        "id",
        "kategori_kelompok",
        "item",
        "modifier_code",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "modifier_code"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the kptl_modifier table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS kptl_modifier (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kategori_kelompok TEXT NOT NULL,
                item TEXT NOT NULL,
                modifier_code TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[KptlModifier]:
        """Find KptlModifier entry by modifier_code."""
        return super().find_by_code(code)  # type: ignore[return-value]
