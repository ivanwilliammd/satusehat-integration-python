"""
Kode Wilayah Indonesia (Indonesian Geographic Codes) terminology model.

Ported from: Satusehat\Integration\Terminology\KodeWilayahIndonesia
Source: satusehat-integration (Laravel)

@property str kode_wilayah
@property str nama_wilayah
@property int level
@property str|None parent
@property str|None state
@property bool active
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class KodeWilayahIndonesia(TerminologyBase):
    """
    Kode Wilayah Indonesia geographic codes.

    Ported from Laravel Eloquent model KodeWilayahIndonesia.
    Table: kode_wilayah_indonesia.

    Level hierarchy: 1=Provinsi, 2=Kabupaten, 3=Kecamatan, 4=Desa/Kelurahan.
    """

    table_name: str = "kode_wilayah_indonesia"
    columns: list[str] = [
        "id",
        "level",
        "kode_wilayah",
        "nama_wilayah",
        "parent",
        "state",
        "active",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "kode_wilayah"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the kode_wilayah_indonesia table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS kode_wilayah_indonesia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level INTEGER,
                kode_wilayah TEXT NOT NULL,
                nama_wilayah TEXT NOT NULL,
                parent TEXT,
                state TEXT,
                active INTEGER DEFAULT 1,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wilayah_code ON kode_wilayah_indonesia(kode_wilayah)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wilayah_level ON kode_wilayah_indonesia(level)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wilayah_parent ON kode_wilayah_indonesia(parent)"
        )
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[KodeWilayahIndonesia]:
        """Find KodeWilayah entry by kode_wilayah."""
        return super().find_by_code(code)  # type: ignore[return-value]

    @classmethod
    def find_by_level(cls, level: int) -> list[KodeWilayahIndonesia]:
        """Find all entries for a given administrative level."""
        conn = cls.get_connection()
        rows = conn.execute(
            "SELECT * FROM kode_wilayah_indonesia WHERE level = ?", (level,)
        ).fetchall()
        return [cls._row_to_instance(r) for r in rows]  # type: ignore[return-value]

    @classmethod
    def find_provinces(cls) -> list[KodeWilayahIndonesia]:
        """Find all provinces (level=1)."""
        return cls.find_by_level(1)  # type: ignore[return-value]

    @classmethod
    def find_by_parent(cls, parent: str) -> list[KodeWilayahIndonesia]:
        """Find all children of a given parent."""
        conn = cls.get_connection()
        rows = conn.execute(
            "SELECT * FROM kode_wilayah_indonesia WHERE parent = ?", (parent,)
        ).fetchall()
        return [cls._row_to_instance(r) for r in rows]  # type: ignore[return-value]
