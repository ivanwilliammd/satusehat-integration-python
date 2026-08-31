"""
LOINC Answer List terminology model.

Ported from: Satusehat\Integration\Terminology\LoincAnswer
Source: satusehat-integration (Laravel)

@property str LoincNumber
@property str AnswerListId
@property str AnswerListName
@property str AnswerStringId
@property int SequenceNumber
@property str DisplayText
@property str ExtCodeId
@property str ExtCodeDisplayName
@property str ExtCodeSystem
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class LoincAnswer(TerminologyBase):
    """
    LOINC Answer List for coded observation answers.

    Ported from Laravel Eloquent model LoincAnswer.
    Table: satusehat_loinc_answer.
    """

    table_name: str = "satusehat_loinc_answer"
    columns: list[str] = [
        "id",
        "LoincNumber",
        "AnswerListId",
        "AnswerListName",
        "AnswerStringId",
        "SequenceNumber",
        "DisplayText",
        "ExtCodeId",
        "ExtCodeDisplayName",
        "ExtCodeSystem",
        "created_at",
        "updated_at",
        "deleted_at",
    ]
    primary_key: str = "id"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the satusehat_loinc_answer table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS satusehat_loinc_answer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                LoincNumber TEXT,
                AnswerListId TEXT,
                AnswerListName TEXT,
                AnswerStringId TEXT,
                SequenceNumber INTEGER,
                DisplayText TEXT,
                ExtCodeId TEXT,
                ExtCodeDisplayName TEXT,
                ExtCodeSystem TEXT,
                created_at TEXT,
                updated_at TEXT,
                deleted_at TEXT
            )
        """)
        conn.commit()
