"""Hasilkan/rapikan parser Python dari builder.

Alasan sama seperti repo PHP dan Node: getter dengan nama elemen yang salah tidak melempar apa pun,
hanya mengembalikan None. Daftar elemen diturunkan dari builder — satu-satunya tempat yang tahu
elemen apa yang bisa ditulis.

Aturan:
- Berkas baru dibuat utuh (snake_case + alias camelCase, seperti parser yang sudah ada).
- Berkas lama tidak ditimpa: getter yang belum ada ditambahkan di akhir badan kelas.
- Jalankan: python3 scripts/generate_parsers.py [--check]
"""
import pathlib
import re
import sys

AKAR = pathlib.Path(__file__).resolve().parents[1]
BUILDER = AKAR / "satusehat_integration" / "builder"
PARSER = AKAR / "satusehat_integration" / "parser"

# Dua gaya penulisan builder hidup berdampingan di repo ini: yang memakai BaseBuilder
# (`self._set`/`self._append`) dan yang menulis `self.set`/`self.push` sendiri. Keduanya harus
# terbaca, kalau tidak builder gaya kedua terlewat tanpa suara.
POLA = (
    re.compile(r"self\._set\(\s*\"([^\"]+)\""),
    re.compile(r"self\._append\(\s*\"([^\"]+)\""),
    re.compile(r"self\.set\(\s*\"([^\"]+)\""),
    re.compile(r"self\.push\(\s*\"([^\"]+)\""),
)


def snake(nama: str) -> str:
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", nama)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def resource_dari(teks: str) -> str | None:
    """Nama resource, dari panggilan induk atau dari resourceType yang ditulis langsung.

    Sebagian builder tidak memakai BaseBuilder dan menulis `{"resourceType": "X"}` sendiri; tanpa
    jalur kedua, mereka dilewati generator dan parser-nya tidak pernah ikut diperbarui.
    """
    m = re.search(r"super\(\)\.__init__\(\s*\"([^\"]+)\"", teks)
    if m:
        return m.group(1)
    m = re.search(r'"resourceType"\s*:\s*"([A-Za-z0-9]+)"', teks)
    return m.group(1) if m else None


def elemen_builder(teks: str) -> list[str]:
    kunci: list[str] = []
    for pola in POLA:
        for m in pola.finditer(teks):
            k = m.group(1).split("/")[0]
            if k and k not in kunci and k != "resourceType" and re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", k):
                kunci.append(k)
    return kunci


def modul_dari(resource: str) -> str:
    return "list_resource" if resource == "List" else snake(resource)


def getter(kunci: str) -> str:
    return f"""
    def get_{snake(kunci)}(self) -> Any:
        return self._data.get("{kunci}")

    get{kunci[0].upper() + kunci[1:]} = get_{snake(kunci)}
"""


def kepala(resource: str, field: str) -> str:
    return f'''"""{resource}Parser — pembaca elemen tingkat atas resource FHIR R4 {resource}.

Dihasilkan dari {resource}Builder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class {resource}Parser:
    def __init__(self, data: Optional[dict[str, Any]] = None) -> None:
        self._data: dict[str, Any] = data if isinstance(data, dict) else {{}}

    def get_raw(self) -> dict[str, Any]:
        return self._data

    getRaw = get_raw
'''


def berkas_untuk(resource: str, elemen: list[str]) -> str:
    return kepala(resource, "_data") + "".join(getter(k) for k in elemen)


def getter_ada(teks: str) -> set[str]:
    return set(re.findall(r"def (get_\w+)\(", teks))


def sinkronkan() -> list[str]:
    berubah: list[str] = []
    for path in sorted(BUILDER.glob("*.py")):
        # Berkas uji di direktori builder memuat builder palsu (resourceType "X"); tanpa pengecualian
        # ini, generator membuat parser untuk resource yang tidak ada. Tandanya bukan nama berkas:
        # `test_script.py` dan `test_report.py` adalah builder sungguhan untuk TestScript/TestReport.
        if path.name.startswith("_") or path.name == "base_builder.py":
            continue
        isi = path.read_text(encoding="utf-8")
        if "\ndef test_" in isi:
            continue
        teks = path.read_text()
        resource = resource_dari(teks)
        if not resource:
            continue
        elemen = elemen_builder(teks)
        tujuan = PARSER / f"{modul_dari(resource)}_parser.py"
        if not tujuan.exists():
            tujuan.write_text(berkas_untuk(resource, elemen), encoding="utf-8")
            berubah.append(f"baru   {tujuan.name}")
            continue
        lama = tujuan.read_text()
        ada = getter_ada(lama)
        kurang = [k for k in elemen if f"get_{snake(k)}" not in ada]
        if not kurang:
            continue
        tujuan.write_text(lama.rstrip() + "\n" + "".join(getter(k) for k in kurang), encoding="utf-8")
        berubah.append(f"tambah {tujuan.name} ({len(kurang)} getter)")
    return berubah


def main() -> int:
    n = sinkronkan()
    if "--check" in sys.argv:
        if n:
            print("parser belum sinkron:")
            print("\n".join(n[:20]))
            return 1
        print("parser sinkron")
        return 0
    print(f"{len(n)} berkas diubah")
    print("\n".join(n[:10]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
