"""Permukaan method kanon PHP vs builder Python — dari kontrak yang di-commit, bukan checkout.

Daftar method kanon ada di `contracts/php_method_surface.json`. Berkas itu dihasilkan dari
PayloadBuilder*.php dan ikut ter-commit, sehingga uji ini berjalan penuh di CI tanpa perlu
checkout repo PHP (privat) maupun token.

Bila checkout PHP tersedia (mesin pengembang), uji kedua memastikan manifest masih sama dengan
kanon — kalau kanon berubah dan manifest tidak diperbarui, itu kegagalan, bukan diam.

Regenerate manifest:
    python -c "import json,re,pathlib; ..."  (lihat scripts/perbarui_kontrak.py)
"""
import json
import os
import pathlib
import re

import pytest

AKAR = pathlib.Path(__file__).resolve().parents[2]
KONTRAK = AKAR / "contracts" / "php_method_surface.json"
PY = pathlib.Path(__file__).resolve().parent
PHP = pathlib.Path(os.environ.get("PHP_BUILDER_DIR", "/home/openclaw/projects/satusehat-integration/src/Builder"))

# Method kanon yang memang tidak diporting, beserta alasannya.
DIPERBOLEHKAN = {
    ("Bundle", "json"): "mengembalikan string JSON, bukan mengubah payload; Python memakai build()",
}


def snake(nama: str) -> str:
    """setTotalVAT -> set_total_vat, bukan set_total_v_a_t."""
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", nama)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


def snake_resource(rt: str) -> str:
    # Nama resource FHIR "List" bertabrakan dengan tipe bawaan Python.
    return "list_resource" if rt == "List" else snake(rt)


def muat_kontrak() -> dict:
    return json.loads(KONTRAK.read_text())


def pasangan():
    kontrak = muat_kontrak()
    return [(rt, m) for rt in sorted(kontrak) for m in kontrak[rt]]


@pytest.mark.parametrize("resource,method", pasangan())
def test_method_kanon_ada_di_python(resource, method):
    if (resource, method) in DIPERBOLEHKAN:
        pytest.skip(DIPERBOLEHKAN[(resource, method)])
    berkas = PY / f"{snake_resource(resource)}.py"
    assert berkas.exists(), f"builder Python untuk {resource} belum ada"
    defs = set(re.findall(r"def (\w+)\(", berkas.read_text()))
    assert snake(method) in defs, f"{resource}: {snake(method)} belum ada di {berkas.name}"


@pytest.mark.skipif(not PHP.is_dir(), reason="checkout kanon PHP tidak ada di mesin ini")
def test_manifest_sama_dengan_kanon_php():
    """Manifest harus persis sama dengan kanon; kalau tidak, ia jadi kontrak yang sudah basi."""
    nyata = {}
    for path in sorted(PHP.glob("PayloadBuilder*.php")):
        teks = path.read_text()
        rt = re.search(r"resourceType\s*=\s*'([^']+)'", teks).group(1)
        nyata[rt] = sorted({m for m in re.findall(r"public function (\w+)\(", teks) if m not in ("__construct", "build")})
    assert nyata == muat_kontrak()
