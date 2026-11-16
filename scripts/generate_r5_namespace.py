"""Siapkan namespace R5 sebagai lapisan tipis di atas kelas kanon R4 (Python).

Memakai R5 cukup dengan mengganti baris `import`:

    from src.builder.basic import BasicBuilder        # R4
    from src.r5.builder.basic import BasicBuilder     # R5 — hanya baris ini

Setiap kelas R5 adalah turunan apa adanya dari kelas kanon selama R5 tidak mengubahnya. Bila satu
resource memang berbeda di R5, hapus penanda `@generated` pada berkas itu dan tulis implementasinya;
generator berhenti menyentuhnya.

Jalankan: python3 scripts/generate_r5_namespace.py [--check]
"""
import pathlib
import re
import sys

AKAR = pathlib.Path(__file__).resolve().parents[1]
SUMBER = {"builder": AKAR / "src" / "builder", "datatype": AKAR / "src" / "datatype"}
TUJUAN = AKAR / "src" / "r5"


def kelas_dari(berkas: pathlib.Path) -> str | None:
    m = re.search(r"^class (\w+)", berkas.read_text(), re.M)
    return m.group(1) if m else None


def isi(ruang: str, modul: str, nama: str) -> str:
    return f'''"""@generated oleh scripts/generate_r5_namespace.py — jangan disunting tangan.

Lapisan R5: turunan apa adanya dari kelas kanon (R4). Selama R5 tidak mengubah resource ini,
memakai R5 cukup dengan mengganti baris import. Bila R5 memang berbeda, hapus penanda @generated
dan tulis implementasinya di sini.
"""
from __future__ import annotations

from src.{ruang}.{modul} import {nama} as _R4{nama}


class {nama}(_R4{nama}):
    """R5: belum ada perbedaan terverifikasi terhadap R4."""
'''


def sinkronkan() -> list[str]:
    berubah: list[str] = []
    for ruang, direktori in SUMBER.items():
        (TUJUAN / ruang).mkdir(parents=True, exist_ok=True)
        init = TUJUAN / ruang / "__init__.py"
        if not init.exists():
            init.write_text("", encoding="utf-8")
        for berkas in sorted(direktori.glob("*.py")):
            if berkas.name.startswith("_"):
                continue
            nama = kelas_dari(berkas)
            if not nama:
                continue
            tujuan = TUJUAN / ruang / berkas.name
            baru = isi(ruang, berkas.stem, nama)
            if not tujuan.exists():
                tujuan.write_text(baru, encoding="utf-8")
                berubah.append(f"baru   r5/{ruang}/{berkas.name}")
                continue
            lama = tujuan.read_text(encoding="utf-8").replace("\r\n", "\n")
            if "@generated" not in lama:
                continue
            if lama != baru:
                tujuan.write_text(baru, encoding="utf-8", newline="\n")
                berubah.append(f"ubah   r5/{ruang}/{berkas.name}")
    for paket in (TUJUAN, TUJUAN / "builder", TUJUAN / "datatype"):
        init = paket / "__init__.py"
        if not init.exists():
            init.write_text("", encoding="utf-8")
    return berubah


def main() -> int:
    n = sinkronkan()
    if "--check" in sys.argv:
        if n:
            print("namespace R5 belum sinkron:")
            print("\n".join(n[:20]))
            return 1
        print("namespace R5 sinkron")
        return 0
    print(f"{len(n)} berkas diubah")
    print("\n".join(n[:8]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
