r"""
UCUM (Units of Measure) terminology model.

Ported from: Satusehat\Integration\Terminology\Ucum
Source: satusehat-integration (Laravel)

@property str code
@property str descriptive_name
@property str code_system
@property str definition
@property str date_created
@property str synonym
@property str status
@property str kind_of_quantity
@property str date_revised
@property str concept_id
@property str dimension
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class Ucum(TerminologyBase):
    """
    UCUM units of measure terminology.

    Ported from Laravel Eloquent model Ucum.
    Table: satusehat_ucum.
    """

    table_name: str = "satusehat_ucum"
    columns: list[str] = [
        "id",
        "code",
        "descriptive_name",
        "code_system",
        "definition",
        "date_created",
        "synonym",
        "status",
        "kind_of_quantity",
        "date_revised",
        "concept_id",
        "dimension",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "code"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the satusehat_ucum table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS satusehat_ucum (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                descriptive_name TEXT NOT NULL,
                code_system TEXT NOT NULL,
                definition TEXT,
                date_created TEXT,
                synonym TEXT,
                status TEXT NOT NULL,
                kind_of_quantity TEXT NOT NULL,
                date_revised TEXT,
                concept_id TEXT NOT NULL,
                dimension TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.commit()
