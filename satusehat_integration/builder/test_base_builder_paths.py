"""Jalur bertingkat di BaseBuilder: satu helper, bukan workaround per kelas."""
from satusehat_integration.builder.base_builder import BaseBuilder


def test_set_jalur_menulis_objek_bersarang():
    b = BaseBuilder("X")._set("period/start", "2026-01-01")._set("period/end", "2026-01-02")
    assert b.build() == {"resourceType": "X", "period": {"start": "2026-01-01", "end": "2026-01-02"}}


def test_set_jalur_tidak_meninggalkan_kunci_literal():
    b = BaseBuilder("X")._set("a/b", 1)
    assert "a/b" not in b.build()


def test_push_jalur_menumpuk_di_dalam_objek():
    b = BaseBuilder("X")._push("meta/profile", "https://x/1")._push("meta/profile", "https://x/2")
    assert b.build()["meta"]["profile"] == ["https://x/1", "https://x/2"]


def test_segmen_angka_menunjuk_elemen_daftar_yang_dibuat_seperlunya():
    b = BaseBuilder("X")._push("item", {"a": 1})._set("item/0/b", 2)._set("item/2/c", 3)
    assert b.build()["item"][0] == {"a": 1, "b": 2}
    assert b.build()["item"][2] == {"c": 3}


def test_nilai_kosong_tetap_dilewati():
    b = BaseBuilder("X")._set("active", False)._set("kosong", "")
    assert b.build()["active"] is False
    assert "kosong" not in b.build()
