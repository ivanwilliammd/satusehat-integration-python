"""Penjaga elemen tingkat atas terhadap definisi FHIR R4 resmi.

Sebagian builder bisa menulis elemen yang tidak ada di resource-nya (mis. ``onsetDateTime`` pada
``Goal``). Payload seperti itu sah secara JSON, hanya bukan R4 — dan server menolaknya tanpa pesan
yang berguna.

Pemeriksaan opt-in (``SATUSEHAT_STRICT_R4=1``) karena menyalakannya bawaan akan menggagalkan
pemanggil yang sudah memakai setter lama.
"""
from __future__ import annotations

import os
from typing import Any, Mapping

from ._r4_elements_generated import ELEMEN

# Nama resource yang berbeda antara kelas builder dan definisi FHIR.
_ALIAS = {"ListResource": "List"}

_FALSE = {"", "0", "false", "off", "no"}


def unknown_elements(payload: Mapping[str, Any]) -> list[str]:
    """Elemen tingkat atas yang tidak ada di R4 untuk payload ini."""
    tipe = payload.get("resourceType")
    if not isinstance(tipe, str) or not tipe:
        return ["resourceType"]

    sah = set(ELEMEN.get(_ALIAS.get(tipe, tipe), ()))
    if not sah:
        # Resource di luar definisi R4: tidak ada dasar untuk memeriksa.
        return []

    return sorted(k for k in payload if k != "resourceType" and k not in sah)


def assert_r4_elements(payload: Mapping[str, Any]) -> None:
    """Lempar ``ValueError`` bila ada elemen asing."""
    asing = unknown_elements(payload)
    if not asing:
        return
    tipe = payload.get("resourceType")
    nama = tipe if isinstance(tipe, str) else "(tanpa resourceType)"
    raise ValueError(f"{nama} menulis elemen yang tidak ada di FHIR R4: {', '.join(asing)}")


def strict_r4_enabled() -> bool:
    """``SATUSEHAT_STRICT_R4=1`` (atau true/on/yes) menyalakan pemeriksaan."""
    return os.environ.get("SATUSEHAT_STRICT_R4", "").strip().lower() not in _FALSE
