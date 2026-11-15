"""Setiap method publik di builder PHP harus ada di builder Python dengan nama snake_case.

Uji ini menjaga PERMUKAAN method, bukan perilaku — perilaku dijaga golden per resource.
Kalau kanon menambah setter baru, uji ini berbunyi sebelum ada yang menyadarinya.
"""
import pathlib
import re

import pytest

PHP = pathlib.Path("/home/openclaw/projects/satusehat-integration/src/Builder")
PY = pathlib.Path(__file__).resolve().parent

# Method kanon yang memang tidak diporting, beserta alasannya.
DIPERBOLEHKAN = {
    ("Bundle", "json"): "mengembalikan string JSON, bukan mengubah payload; Python memakai build()",
    ("List", "setId"): "builder List belum ada di Python (resource FHIR bernama List)",
}


def snake(nama: str) -> str:
    """setTotalVAT -> set_total_vat, bukan set_total_v_a_t."""
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", nama)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


def snake_resource(rt: str) -> str:
    # Nama resource FHIR "List" bertabrakan dengan tipe bawaan Python.
    return "list_resource" if rt == "List" else snake(rt)


def pasangan():
    hasil = []
    for path in sorted(PHP.glob("PayloadBuilder*.php")):
        teks = path.read_text()
        rt = re.search(r"resourceType\s*=\s*'([^']+)'", teks).group(1)
        for m in re.findall(r"public function (\w+)\(", teks):
            if m not in ("__construct", "build"):
                hasil.append((rt, m))
    return hasil


@pytest.mark.parametrize("resource,method", pasangan())
def test_method_kanon_ada_di_python(resource, method):
    if (resource, method) in DIPERBOLEHKAN:
        pytest.skip(DIPERBOLEHKAN[(resource, method)])
    berkas = PY / f"{snake_resource(resource)}.py"
    assert berkas.exists(), f"builder Python untuk {resource} belum ada"
    defs = set(re.findall(r"def (\w+)\(", berkas.read_text()))
    assert snake(method) in defs, f"{resource}: {snake(method)} belum ada di {berkas.name}"
