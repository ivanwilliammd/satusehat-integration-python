"""Uji kesiapan namespace R5 (Python).

Janji ke pemakai: mengganti `from src.builder.x import XBuilder` menjadi
`from src.r5.builder.x import XBuilder` tidak mengubah apa pun selain baris import.

Yang diperiksa: kelas R5 ada, ia turunan langsung kelas kanon, dan setiap method publik kanon
diwarisi apa adanya (bukan disalin, bukan ditimpa).
"""
from __future__ import annotations

import importlib
import inspect
import subprocess
import sys
from pathlib import Path

import pytest

AKAR = Path(__file__).resolve().parents[2]
BUILDER = AKAR / "src" / "builder"


def daftar() -> list[tuple[str, str]]:
    hasil = []
    for berkas in sorted(BUILDER.glob("*.py")):
        if berkas.name.startswith("_") or berkas.name.startswith("test_") or berkas.name == "base_builder.py":
            continue
        teks = berkas.read_text()
        for baris in teks.splitlines():
            if baris.startswith("class "):
                nama = baris.split()[1].split("(")[0].rstrip(":")
                hasil.append((berkas.stem, nama))
                break
    return hasil


KASUS = daftar()


@pytest.mark.parametrize("modul,nama", KASUS, ids=[f"{m}.{n}" for m, n in KASUS])
def test_r5_turunan_kanon(modul: str, nama: str) -> None:
    kanon = importlib.import_module(f"src.builder.{modul}")
    r5 = importlib.import_module(f"src.r5.builder.{modul}")

    K4 = getattr(kanon, nama)
    K5 = getattr(r5, nama, None)
    assert K5 is not None, f"src/r5/builder/{modul}.py tidak mengekspor {nama}"
    assert K5.__bases__ == (K4,), f"{nama} R5 bukan turunan langsung kanon"

    metode = [m for m in vars(K4) if not m.startswith("_") and inspect.isfunction(getattr(K4, m))]
    beda = [m for m in metode if getattr(K5, m) is not getattr(K4, m)]
    assert not beda, f"{nama}: method tidak diwarisi apa adanya: {', '.join(beda)}"


def test_r5_sinkron() -> None:
    hasil = subprocess.run(
        [sys.executable, str(AKAR / "scripts" / "generate_r5_namespace.py"), "--check"],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert hasil.returncode == 0, hasil.stdout + hasil.stderr
