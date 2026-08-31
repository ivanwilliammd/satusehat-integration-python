"""
KFA (Katalog Farmasi Alat Kesehatan) terminology model.

Ported from: Satusehat\Integration\Terminology\Kfa
Source: satusehat-integration (Laravel)

@property str kfa_code
@property str product_template
@property str display_name
@property str brand
@property str uom_drug_form
@property str drug_form_hl7
@property str medication_form
@property str medication_form_code
@property int logistic_dose
@property str drug_class
@property str atc_class
@property bool fornas
@property float lkpp_price
@property str izin_edar
@property float het
@property str manufacturer
@property bool lkpp_show
@property str tag
@property str status
@property str|None created_at
@property str|None updated_at
"""
from __future__ import annotations

from typing import Any, Optional

from .base import TerminologyBase


class Kfa(TerminologyBase):
    """
    KFA (Katalog Farmasi Alat Kesehatan) medication product codes.

    Ported from Laravel Eloquent model Kfa.
    Table: satusehat_kfa.
    """

    table_name: str = "satusehat_kfa"
    columns: list[str] = [
        "id",
        "kfa_code",
        "product_template",
        "display_name",
        "brand",
        "uom_drug_form",
        "drug_form_hl7",
        "medication_form",
        "medication_form_code",
        "logistic_dose",
        "drug_class",
        "atc_class",
        "fornas",
        "lkpp_price",
        "izin_edar",
        "het",
        "manufacturer",
        "lkpp_show",
        "tag",
        "status",
        "created_at",
        "updated_at",
    ]
    primary_key: str = "id"
    code_column: str = "kfa_code"

    def __init__(self, **attrs: Any):
        super().__init__(**attrs)

    @classmethod
    def create_table(cls) -> None:
        """Create the satusehat_kfa table."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS satusehat_kfa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kfa_code TEXT NOT NULL,
                product_template TEXT NOT NULL,
                display_name TEXT NOT NULL,
                brand TEXT NOT NULL,
                uom_drug_form TEXT NOT NULL,
                drug_form_hl7 TEXT NOT NULL,
                medication_form TEXT NOT NULL,
                medication_form_code TEXT NOT NULL,
                logistic_dose INTEGER NOT NULL,
                drug_class TEXT NOT NULL,
                atc_class TEXT NOT NULL,
                fornas INTEGER DEFAULT 0,
                lkpp_price REAL,
                izin_edar TEXT,
                het REAL,
                manufacturer TEXT NOT NULL,
                lkpp_show INTEGER DEFAULT 0,
                tag TEXT,
                status TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.commit()

    @classmethod
    def find_by_code(cls, code: str) -> Optional[Kfa]:
        """Find KFA entry by kfa_code."""
        return super().find_by_code(code)  # type: ignore[return-value]
