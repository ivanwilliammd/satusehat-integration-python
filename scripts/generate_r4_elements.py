"""Salin data/r4_elements.json (repo PHP) menjadi modul Python.

Angka elemen sah tidak boleh diketik tangan: satu salah ketik menghasilkan penjaga yang menolak
payload benar, dan itu lebih buruk daripada tidak ada penjaga.

Pakai: python3 scripts/generate_r4_elements.py ../satusehat-integration/data/r4_elements.json
"""
import json
import pathlib
import sys

sumber = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                      "../satusehat-integration/data/r4_elements.json")
tujuan = pathlib.Path(__file__).resolve().parents[1] / "src" / "conformance" / "_r4_elements_generated.py"

data = json.loads(sumber.read_text(encoding="utf-8"))
bersih = {nama: sorted(daftar) for nama, daftar in sorted(data.items())}

kepala = (
    '"""BERKAS INI DIGENERATE — jangan disunting tangan.\n\n'
    "Sumber: data/r4_elements.json di repo PHP (dihasilkan scripts/generate_r4_elements.py dari\n"
    "profiles-resources.json HL7 R4 resmi). Disalin sebagai modul Python karena setuptools tidak\n"
    "menjamin berkas JSON ikut terpasang. Perbarui dengan scripts/generate_r4_elements.py.\n"
    '"""\n\n'
)
tujuan.write_text(kepala + "ELEMEN = " + repr(bersih) + "\n", encoding="utf-8")
print(f"{len(bersih)} resource ditulis ke {tujuan}")
