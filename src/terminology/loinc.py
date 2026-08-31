"""
LOINC terminology model.

Ported from: Satusehat\Integration\Terminology\Loinc
Source: satusehat-integration (Laravel)

@property str LOINC_NUM
@property str COMPONENT
@property str PROPERTY
@property str TIME_ASPCT
@property str SYSTEM
@property str SCALE_TYP
@property str METHOD_TYP
@property str CLASS
@property str CLASSTYPE
@property str LONG_COMMON_NAME
@property str SHORTNAME
@property str EXTERNAL_COPYRIGHT_NOTICE
@property str STATUS
@property str VersionFirstReleased
@property str VersionLastChanged
@property str|None created_at
@property str|None updated_at
@property str|None deleted_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class Loinc(TerminologyBase):
    """
    LOINC terminology codes for observations and measurements.

    Ported from Laravel Eloquent model Loinc.
    Table: satusehat_loinc.
    """

    table_name: str = "satusehat_loinc"
    columns: list[str] = [
        "id",
        "LOINC_NUM",
        "COMPONENT",
        "PROPERTY",
        "TIME_ASPCT",
        "SYSTEM",
        "SCALE_TYP",
        "METHOD_TYP",
        "CLASS",
        "CLASSTYPE",
        "LONG_COMMON_NAME",
        "SHORTNAME",
        "EXTERNAL_COPYRIGHT_NOTICE",
        "STATUS",
        "VersionFirstReleased",
        "VersionLastChanged",
        "created_at",
        "updated_at",
        "deleted_at",
    ]
    primary_key: str = "id"
    code_column: str = "LOINC_NUM"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the satusehat_loinc table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS satusehat_loinc (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                LOINC_NUM TEXT UNIQUE NOT NULL,
                COMPONENT TEXT,
                PROPERTY TEXT,
                TIME_ASPCT TEXT,
                SYSTEM TEXT,
                SCALE_TYP TEXT,
                METHOD_TYP TEXT,
                CLASS TEXT,
                CLASSTYPE TEXT,
                LONG_COMMON_NAME TEXT,
                SHORTNAME TEXT,
                EXTERNAL_COPYRIGHT_NOTICE TEXT,
                STATUS TEXT,
                VersionFirstReleased TEXT,
                VersionLastChanged TEXT,
                created_at TEXT,
                updated_at TEXT,
                deleted_at TEXT
            )
        """)
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_loinc_num ON satusehat_loinc(LOINC_NUM)")
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[Loinc]:
        """Find LOINC entry by LOINC number."""
        return super().find_by_code(code)  # type: ignore[return-value]
