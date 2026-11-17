"""Aturan wajib SATUSEHAT yang bisa diputuskan dari payload saja.

Audit R4 menjawab "apakah elemen ini ada di R4"; ia tidak menjawab "apakah isinya bentuk yang diterima
SATUSEHAT". Aturannya tidak ditulis di sini: `data/satusehat/required-rules.json` memuat tiap butir
bersama URL dokumentasi sumbernya, dan modul ini hanya menjalankan butir itu. Menambah resource berarti
menambah data, bukan kode.

Yang tidak diklaim: aturan yang butuh data di luar payload (mis. identifier organisasi harus terdaftar
di master sarana).
"""
from __future__ import annotations

from typing import Any

from ._rules_generated import RULES, RULES_SHA

ACT_CODE = "http://terminology.hl7.org/CodeSystem/v3-ActCode"

ENCOUNTER_STATUS = (
    "planned",
    "arrived",
    "triaged",
    "in-progress",
    "onleave",
    "finished",
    "cancelled",
    "entered-in-error",
    "unknown",
)

OBSERVATION_STATUS = (
    "registered",
    "preliminary",
    "final",
    "amended",
    "corrected",
    "cancelled",
    "entered-in-error",
    "unknown",
)

PROCEDURE_STATUS = (
    "preparation",
    "in-progress",
    "not-done",
    "on-hold",
    "stopped",
    "completed",
    "entered-in-error",
    "unknown",
)


def _ambil(payload: dict[str, Any], jalur: str) -> Any:
    simpul: Any = payload
    for kunci in jalur.split("."):
        if not isinstance(simpul, dict) or kunci not in simpul:
            return None
        simpul = simpul[kunci]
    return simpul


def _kosong(nilai: Any) -> bool:
    if nilai is None:
        return True
    if isinstance(nilai, (str, list, dict, tuple)):
        return len(nilai) == 0
    return False


def _periksa(payload: dict[str, Any], resource: str, butir: dict[str, Any]) -> str | None:
    elemen = butir["elemen"]
    nilai = _ambil(payload, elemen.replace("[x]", ""))
    sebut = f"{resource}.{elemen}"
    # SATUSEHAT mewajibkan encounter pada beberapa resource yang di R4 opsional. Alasannya ditulis di
    # pesan supaya tidak dikira pustaka ini salah membaca spesifikasi.
    catatan_r4 = " (SATUSEHAT, meski opsional di R4)" if elemen == "encounter" else ""
    jenis = butir["jenis"]

    if jenis == "kode":
        return None if isinstance(nilai, str) and nilai in butir["kode"] else (
            f"{sebut} bukan kode yang sah: {nilai if isinstance(nilai, str) else '(kosong)'}"
        )
    if jenis == "isi":
        return None if not _kosong(nilai) else f"{sebut} wajib diisi"
    if jenis == "ada":
        return None if nilai is not None else f"{sebut} wajib ada{catatan_r4}"
    if jenis == "referensi":
        acuan = nilai.get("reference") if isinstance(nilai, dict) else None
        return None if isinstance(acuan, str) and acuan.startswith(butir["awalan"]) else (
            f"{sebut} wajib merujuk {butir['awalan']}"
        )
    if jenis == "sistem":
        langsung = nilai.get("system") if isinstance(nilai, dict) else None
        bersarang = None
        if isinstance(nilai, dict):
            coding = nilai.get("coding")
            if isinstance(coding, list) and coding and isinstance(coding[0], dict):
                bersarang = coding[0].get("system")
        return None if (langsung or bersarang) == butir["sistem"] else (
            f"{sebut} wajib system {butir['sistem']}"
        )
    if jenis == "salah_satu":
        return None if any(pilihan in payload for pilihan in butir["pilihan"]) else (
            f"{sebut} wajib salah satu: {', '.join(butir['pilihan'])}"
        )

    raise ValueError(f"Jenis aturan tidak dikenal: {jenis}")


def violations(payload: dict[str, Any]) -> list[str]:
    """Daftar pelanggaran; kosong berarti lolos."""
    resource = payload.get("resourceType")
    if not isinstance(resource, str) or resource == "":
        return ["resourceType tidak ada"]

    masalah: list[str] = []
    for butir in RULES.get(resource, []):
        pesan = _periksa(payload, resource, butir)
        if pesan is not None:
            masalah.append(pesan)
    return masalah
