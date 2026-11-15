"""Kontrak lintas-SDK: jalankan golden/builder/*.input.json terhadap builder Python.

Kasus dan hasil harapan tinggal di repo satusehat-conformance, bukan di sini — supaya lima SDK
diuji terhadap satu kontrak, bukan terhadap asumsinya masing-masing.

Berkas spec memakai bentuk language-neutral:
    {"resource": "Patient", "calls": [{"method": "setId", "args": ["1000000001"]}, ...]}

Datatype bertipe ditulis {"$type": "Identifier", "system": ..., "value": ...}. Runner Python
membuang "$type" dan menyerahkan objek polos, karena builder Python menerima dict.
"""
import importlib
import json
import os
from pathlib import Path

import pytest

KONFORMANSI = Path(os.environ.get("CONFORMANCE_DIR", "/home/openclaw/projects/satusehat-conformance"))
BUILDER_DIR = KONFORMANSI / "golden" / "builder"

KASUS = sorted(BUILDER_DIR.glob("*.input.json")) if BUILDER_DIR.exists() else []


def tanpa_tipe(nilai):
    """Buang penanda $type; builder Python memakai dict polos."""
    if isinstance(nilai, list):
        return [tanpa_tipe(v) for v in nilai]
    if isinstance(nilai, dict):
        return {k: tanpa_tipe(v) for k, v in nilai.items() if k != "$type"}
    return nilai


def snake(nama: str) -> str:
    """setMetaProfile -> set_meta_profile, setVATTotal -> set_vat_total."""
    import re

    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", nama)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def kelas_builder(resource: str):
    modul = "list_resource" if resource == "List" else "".join(
        "_" + c.lower() if c.isupper() else c for c in resource
    ).lstrip("_")
    m = importlib.import_module(f"src.builder.{modul}")
    for nama in (f"{resource}Builder", f"{resource}ResourceBuilder", resource):
        if hasattr(m, nama):
            return getattr(m, nama)
    raise AssertionError(f"builder Python untuk {resource} tidak ditemukan di src/builder/{modul}.py")


@pytest.mark.skipif(not KASUS, reason="repo satusehat-conformance tidak tersedia")
@pytest.mark.parametrize("berkas", KASUS, ids=lambda p: p.name.replace(".input.json", ""))
def test_kasus_konformansi(berkas):
    spec = json.loads(berkas.read_text())
    harapan = json.loads(berkas.with_name(berkas.name.replace(".input.json", ".json")).read_text())

    builder = kelas_builder(spec["resource"])()
    for panggilan in spec["calls"]:
        metode = panggilan["method"]
        nama = metode if hasattr(builder, metode) else snake(metode)
        getattr(builder, nama)(*[tanpa_tipe(a) for a in panggilan.get("args", [])])

    assert builder.build() == harapan
