r"""
KPTL Kamar (Room/Service) terminology model.

Ported from: Satusehat\Integration\Terminology\KptlKamar
Source: satusehat-integration (Laravel)

@property str nama_tindakan_dan_layanan
@property str base_code
@property str allowed_modifiers
@property str kode_kptl
@property str display
@property str code_system
@property str version
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class KptlKamar(TerminologyBase):
    """
    KPTL Kamar (Room/Service) procedure service codes.

    Ported from Laravel Eloquent model KptlKamar.
    Table: kptl_kamar.
    """

    table_name: str = "kptl_kamar"
    columns: list[str] = [
        "id",
        "nama_tindakan_dan_layanan",
        "base_code",
        "allowed_modifiers",
        "kode_kptl",
        "display",
        "code_system",
        "version",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "kode_kptl"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the kptl_kamar table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS kptl_kamar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_tindakan_dan_layanan TEXT NOT NULL,
                base_code TEXT NOT NULL,
                allowed_modifiers TEXT NOT NULL,
                kode_kptl TEXT NOT NULL,
                display TEXT NOT NULL,
                code_system TEXT NOT NULL,
                version TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[KptlKamar]:
        """Find KptlKamar entry by kode_kptl."""
        return super().find_by_code(code)  # type: ignore[return-value]
