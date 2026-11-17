r"""
KemkesTerm terminology model.

Ported from: Satusehat\Integration\Terminology\KemkesTerm
Source: satusehat-integration (Laravel)

@property str resource_type
@property str attribute_path
@property str code
@property str parent_code
@property str display
@property str display_en
@property str code_system
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class KemkesTerm(TerminologyBase):
    """
    Kemenkes (Ministry of Health Indonesia) terminology codes.

    Ported from Laravel Eloquent model KemkesTerm.
    Table: satusehat_kemkesterm.
    """

    table_name: str = "satusehat_kemkesterm"
    columns: list[str] = [
        "id",
        "resource_type",
        "attribute_path",
        "code",
        "parent_code",
        "display",
        "display_en",
        "code_system",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "code"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the satusehat_kemkesterm table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS satusehat_kemkesterm (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_type TEXT NOT NULL,
                attribute_path TEXT NOT NULL,
                code TEXT NOT NULL,
                parent_code TEXT,
                display TEXT NOT NULL,
                display_en TEXT NOT NULL,
                code_system TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[KemkesTerm]:
        """Find KemkesTerm entry by code."""
        return super().find_by_code(code)  # type: ignore[return-value]

    @classmethod
    def find_by_resource_type(cls, resource_type: str) -> list[KemkesTerm]:
        """Find all entries for a given resource type."""
        conn = cls.get_connection()
        rows = conn.execute(
            "SELECT * FROM satusehat_kemkesterm WHERE resource_type = ?",
            (resource_type,),
        ).fetchall()
        return [cls._row_to_instance(r) for r in rows]  # type: ignore[return-value]
