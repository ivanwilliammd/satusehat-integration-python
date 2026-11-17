"""
Base class for SATUSEHAT terminology models.
Provides common CRUD/query operations over a SQLite terminology database.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Default SQLite DB path (user can override via env/config)
DEFAULT_DB_PATH = Path.home() / ".satusehat" / "terminology.db"


class TerminologyBase:
    """
    Base class for terminology models.
    Provides query/search methods against a SQLite terminology database.

    Subclasses must define:
        table_name: str
        columns: list[str]
        primary_key: str  (default 'id')
    """

    table_name: str = ""
    columns: list[str] = []
    primary_key: str = "id"

    _db_path: Optional[Path] = None
    _connection: Optional[sqlite3.Connection] = None

    def __init__(self, db_path: Optional[Path] = None, **attrs: Any):
        self._attrs: dict[str, Any] = {}
        for col in self.columns:
            setattr(self, col, attrs.get(col))
            self._attrs[col] = attrs.get(col)
        # Set id if present
        if self.primary_key in attrs:
            setattr(self, self.primary_key, attrs[self.primary_key])
        if db_path:
            self._db_path = db_path

    @classmethod
    def get_db_path(cls) -> Path:
        """Return the SQLite DB path, creating dir if needed."""
        if cls._db_path is None:
            path = DEFAULT_DB_PATH
            path.parent.mkdir(parents=True, exist_ok=True)
            return path
        return cls._db_path

    @classmethod
    def set_db_path(cls, path: Path) -> None:
        """Set the SQLite DB path for all subclasses."""
        cls._db_path = path
        path.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        """Get a shared DB connection, creating if needed."""
        if cls._connection is None:
            cls._connection = sqlite3.connect(cls.get_db_path())
            cls._connection.row_factory = sqlite3.Row
        return cls._connection

    @classmethod
    def close_connection(cls) -> None:
        """Close the shared DB connection."""
        if cls._connection:
            cls._connection.close()
            cls._connection = None

    @classmethod
    def _row_to_instance(cls, row: sqlite3.Row) -> TerminologyBase:
        """Convert a sqlite3.Row to a model instance."""
        attrs = dict(zip(row.keys(), row))
        return cls(**attrs)

    @classmethod
    def all(cls) -> list[TerminologyBase]:
        """Return all records."""
        conn = cls.get_connection()
        rows = conn.execute(f"SELECT * FROM {cls.table_name}").fetchall()
        return [cls._row_to_instance(r) for r in rows]

    @classmethod
    def count(cls) -> int:
        """Return total record count."""
        conn = cls.get_connection()
        row = conn.execute(f"SELECT COUNT(*) as cnt FROM {cls.table_name}").fetchone()
        return row["cnt"] if row else 0

    @classmethod
    def find(cls, id: Any) -> Optional[TerminologyBase]:
        """Find by primary key."""
        conn = cls.get_connection()
        row = conn.execute(
            f"SELECT * FROM {cls.table_name} WHERE {cls.primary_key} = ?", (id,)
        ).fetchone()
        return cls._row_to_instance(row) if row else None

    @classmethod
    def find_by_code(cls, code: str) -> Optional[TerminologyBase]:
        """Find by code column (subclasses override with their code column)."""
        code_col = getattr(cls, "code_column", cls.primary_key)
        conn = cls.get_connection()
        row = conn.execute(
            f"SELECT * FROM {cls.table_name} WHERE {code_col} = ?", (code,)
        ).fetchone()
        return cls._row_to_instance(row) if row else None

    @classmethod
    def search(cls, query: str) -> list[TerminologyBase]:
        """
        Search across all text columns for the given query string.
        Case-insensitive LIKE search.
        """
        conn = cls.get_connection()
        search_cols = [c for c in cls.columns if c not in ("id", "created_at", "updated_at")]
        conditions = " OR ".join([f"{c} LIKE ?" for c in search_cols])
        pattern = f"%{query}%"
        params = [pattern] * len(search_cols)
        sql = f"SELECT * FROM {cls.table_name} WHERE {conditions} LIMIT 100"
        rows = conn.execute(sql, params).fetchall()
        return [cls._row_to_instance(r) for r in rows]

    @classmethod
    def paginate(
        cls, page: int = 1, per_page: int = 25
    ) -> dict[str, Any]:
        """Return paginated results."""
        offset = (page - 1) * per_page
        conn = cls.get_connection()
        total = cls.count()
        rows = conn.execute(
            f"SELECT * FROM {cls.table_name} LIMIT ? OFFSET ?",
            (per_page, offset),
        ).fetchall()
        return {
            "data": [cls._row_to_instance(r) for r in rows],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    @classmethod
    def create_table(cls) -> None:
        """Create the table if it doesn't exist."""
        raise NotImplementedError("Subclasses must define create_table()")

    @classmethod
    def insert_many(cls, records: list[dict[str, Any]]) -> None:
        """Bulk insert records."""
        if not records:
            return
        conn = cls.get_connection()
        placeholders = ", ".join(["?"] * len(records[0]))
        cols = ", ".join(records[0].keys())
        sql = f"INSERT OR IGNORE INTO {cls.table_name} ({cols}) VALUES ({placeholders})"
        conn.executemany(sql, [tuple(r.values()) for r in records])
        conn.commit()

    def to_dict(self) -> dict[str, Any]:
        """Convert instance to dictionary."""
        return {col: getattr(self, col, None) for col in self.columns}
