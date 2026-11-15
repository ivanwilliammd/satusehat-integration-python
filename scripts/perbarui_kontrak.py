"""Hasilkan ulang contracts/php_method_surface.json dari repo kanon PHP.

Kontrak ini adalah daftar method publik setiap PayloadBuilder*.php. Ia di-commit supaya uji
permukaan bisa berjalan di CI tanpa checkout repo PHP.

Jalankan setiap kali kanon PHP berubah:

    python scripts/perbarui_kontrak.py
    git diff contracts/php_method_surface.json   # periksa apa yang berubah

Bila checkout kanon tidak ada di jalur default, set PHP_BUILDER_DIR.
"""
import json
import os
import pathlib
import re
import sys

KANON = pathlib.Path(
    os.environ.get("PHP_BUILDER_DIR", "/home/openclaw/projects/satusehat-integration/src/Builder")
)
TUJUAN = pathlib.Path(__file__).resolve().parents[1] / "contracts" / "php_method_surface.json"


def main() -> int:
    if not KANON.is_dir():
        print(f"checkout kanon PHP tidak ada di {KANON} (set PHP_BUILDER_DIR)", file=sys.stderr)
        return 2

    kontrak = {}
    for path in sorted(KANON.glob("PayloadBuilder*.php")):
        teks = path.read_text()
        cocok = re.search(r"resourceType\s*=\s*'([^']+)'", teks)
        if not cocok:
            continue
        metode = sorted(
            {m for m in re.findall(r"public function (\w+)\(", teks) if m not in ("__construct", "build")}
        )
        kontrak[cocok.group(1)] = metode

    TUJUAN.parent.mkdir(parents=True, exist_ok=True)
    TUJUAN.write_text(json.dumps(kontrak, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    total = sum(len(v) for v in kontrak.values())
    print(f"{TUJUAN}: {len(kontrak)} resource, {total} method")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
