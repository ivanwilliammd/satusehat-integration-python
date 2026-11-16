"""Uji RATCHET permukaan parser: setiap builder harus punya parser, dan setiap elemen tingkat atas
yang bisa DITULIS builder harus bisa DIBACA kembali.

Yang dijaga bukan perilaku (itu tugas golden), melainkan kesimetrian arah: SDK yang bisa mengirim
`Encounter.status` tetapi tidak bisa membacanya kembali kehilangan separuh gunanya.

Daftar elemen dibaca dari BUILDER, bukan dari parser, supaya uji ini tidak bisa lulus hanya karena
parser dan uji sama-sama melewatkan elemen yang sama.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

BUILDER = Path(__file__).resolve().parents[1] / "builder"
PARSER = Path(__file__).resolve().parent


def snake(nama: str) -> str:
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", nama)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def daftar_builder() -> list[tuple[str, list[str]]]:
    hasil = []
    for path in sorted(BUILDER.glob("*.py")):
        # `test_script.py`/`test_report.py` adalah builder TestScript/TestReport, bukan uji:
        # berkas uji dikenali dari adanya fungsi `def test_` di dalamnya.
        if path.name.startswith("_") or path.name == "base_builder.py":
            continue
        if "\ndef test_" in path.read_text(encoding="utf-8"):
            continue
        teks = path.read_text()
        # Sebagian builder tidak memakai BaseBuilder; resource-nya dibaca dari resourceType.
        m = re.search(r'super\(\)\.__init__\(\s*"([^"]+)"', teks) or re.search(
            r'"resourceType"\s*:\s*"([A-Za-z0-9]+)"', teks
        )
        if not m:
            continue
        elemen: list[str] = []
        for k in re.findall(r'self\.(?:_set|_append|set|push)\(\s*"([^"]+)"', teks):
            akar = k.split("/")[0]
            if akar != "resourceType" and akar not in elemen:
                elemen.append(akar)
        hasil.append((m.group(1), elemen))
    return hasil


KASUS = daftar_builder()


@pytest.mark.parametrize("resource,elemen", KASUS, ids=[k[0] for k in KASUS])
def test_resource_punya_parser_dan_semua_elemen_terbaca(resource: str, elemen: list[str]) -> None:
    modul = "list_resource" if resource == "List" else snake(resource)
    berkas = PARSER / f"{modul}_parser.py"
    assert berkas.exists(), f"parser untuk {resource} belum ada — jalankan scripts/generate_parsers.py"

    teks = berkas.read_text()
    ada = set(re.findall(r"def (get_\w+)\(", teks))
    hilang = [k for k in elemen if f"get_{snake(k)}" not in ada]
    assert not hilang, f"{berkas.name} tidak punya getter untuk: {', '.join(hilang)}"


def test_parser_sinkron_dengan_builder() -> None:
    import subprocess
    import sys

    hasil = subprocess.run(
        [sys.executable, str(PARSER.parents[1] / "scripts" / "generate_parsers.py"), "--check"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert hasil.returncode == 0, hasil.stdout + hasil.stderr
