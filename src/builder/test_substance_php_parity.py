"""Substance: 4 setter PHP (kanon kecil), plus tambahan sah R4."""
import json
from pathlib import Path

import pytest

from src.builder.substance import SubstanceBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"
KFA = "http://sys-ids.kemkes.go.id/kfa"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_scalar_php_golden.json").read_text())


def isi() -> SubstanceBuilder:
    return (
        SubstanceBuilder()
        .set_id("sub-1")
        .set_status("active")
        .set_code(KFA, "93000515", "Amoksisilin")
        .set_text("generated", "<div>Amoksisilin</div>")
    )


def test_sama_dengan_golden_php():
    assert isi().build() == golden("substance")


def test_status_menolak_nilai_di_luar_tiga_yang_sah():
    with pytest.raises(ValueError):
        SubstanceBuilder().set_status("available")


def test_set_code_menerima_objek_maupun_tiga_argumen():
    tiga = SubstanceBuilder().set_code(KFA, "1", "Satu").build()["code"]
    objek = SubstanceBuilder().set_code({"text": "Satu"}).build()["code"]
    assert tiga["coding"][0]["code"] == "1"
    assert objek == {"text": "Satu"}


def test_narrative_ditulis_sebagai_text_dengan_status_dan_div():
    assert isi().build()["text"] == {"status": "generated", "div": "<div>Amoksisilin</div>"}


def test_tambahan_python_tidak_ada_di_kanon():
    kanon = isi().build()
    assert "identifier" not in kanon and "category" not in kanon and "description" not in kanon
    tambahan = SubstanceBuilder().add_identifier("http://x/1", "V1").set_description("Amoksisilin").build()
    assert tambahan["identifier"] == [{"system": "http://x/1", "value": "V1"}]
    assert tambahan["description"] == "Amoksisilin"
