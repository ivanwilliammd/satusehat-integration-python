#!/usr/bin/env python3
"""Hasilkan src/terminology/_rules_generated.py dari data/satusehat/required-rules.json.

Aturan wajib SATUSEHAT disimpan sebagai JSON karena itu bentuk yang bisa dibaca manusia dan dipakai
bersama oleh kelima port. Paket Python tidak memasang berkas data (setuptools tidak menyertakannya),
jadi isinya ditanam sebagai modul Python hasil generate. Uji memastikan berkas hasil generate masih
sama dengan JSON-nya — kalau JSON disunting tanpa menjalankan skrip ini, uji merah.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

AKAR = pathlib.Path(__file__).resolve().parent.parent
SUMBER = AKAR / "data" / "satusehat" / "required-rules.json"
TUJUAN = AKAR / "satusehat_integration" / "terminology" / "_rules_generated.py"

KEPALA = '"""BERKAS INI DIGENERATE — jangan disunting tangan.\n\nSumber: data/satusehat/required-rules.json lewat scripts/generate_rules.py.\nAturan yang sama dipakai kelima port; ubah JSON-nya, lalu jalankan skrip ini.\n"""\nfrom __future__ import annotations\n\nRULES_SHA: str = {sha!r}\n\nRULES: dict[str, list[dict]] = {badan}\n'


def main() -> None:
    mentah = SUMBER.read_bytes()
    isi = json.loads(mentah.decode("utf-8"))
    badan = {k: v for k, v in isi.items() if not k.startswith("_") and isinstance(v, list)}
    sha = hashlib.sha256(mentah).hexdigest()[:16]
    TUJUAN.write_text(KEPALA.format(sha=sha, badan=repr(badan)), encoding="utf-8")
    print(f"{TUJUAN.relative_to(AKAR)}: {len(badan)} resource, sha {sha}")


if __name__ == "__main__":
    main()
