"""Objek non-standar SATUSEHAT — identifier dan extension di luar FHIR R4 inti.

URL di bawah berasal dari dokumentasi resmi SATUSEHAT dan Implementation Guide, bukan karangan.
Payload yang "sah secara R4" masih bisa ditolak karena NIK wajib memakai sistem identifier Kemkes.
"""
from __future__ import annotations

from typing import Any, Iterable, Sequence

NIK_SYSTEM = "https://fhir.kemkes.go.id/id/nik"
PASSPORT_SYSTEM = "https://fhir.kemkes.go.id/id/paspor"
KK_SYSTEM = "https://fhir.kemkes.go.id/id/kk"
IHS_SYSTEM = "https://fhir.kemkes.go.id/id/patient-ihs-number"

EXT_ADMINISTRATIVE_CODE = "https://fhir.kemkes.go.id/r4/StructureDefinition/administrativeCode"
EXT_BIRTH_PLACE = "https://fhir.kemkes.go.id/r4/StructureDefinition/birthPlace"
EXT_CITIZENSHIP_STATUS = "https://fhir.kemkes.go.id/r4/StructureDefinition/citizenshipStatus"
EXT_PATIENT_RELIGION = "https://fhir.kemkes.go.id/r4/StructureDefinition/patient-religion"
EXT_PATIENT_DISABILITY = "https://fhir.kemkes.go.id/r4/StructureDefinition/patient-disability"
EXT_PATIENT_CITIZENSHIP = "https://fhir.kemkes.go.id/r4/StructureDefinition/patient-citizenship"
EXT_PATIENT_BIRTH_TIME = "https://fhir.kemkes.go.id/r4/StructureDefinition/patient-birthTime"

PROFILE_PATIENT = "https://fhir.kemkes.go.id/r4/StructureDefinition/Patient"

ALL: tuple[tuple[str, str], ...] = (
    ("nik", NIK_SYSTEM),
    ("paspor", PASSPORT_SYSTEM),
    ("kk", KK_SYSTEM),
    ("ihs", IHS_SYSTEM),
    ("administrative_code", EXT_ADMINISTRATIVE_CODE),
    ("birth_place", EXT_BIRTH_PLACE),
    ("citizenship_status", EXT_CITIZENSHIP_STATUS),
    ("patient_religion", EXT_PATIENT_RELIGION),
    ("patient_disability", EXT_PATIENT_DISABILITY),
    ("patient_citizenship", EXT_PATIENT_CITIZENSHIP),
    ("patient_birth_time", EXT_PATIENT_BIRTH_TIME),
)


def official_identifier(system: str, value: str) -> dict[str, Any]:
    """Identifier resmi SATUSEHAT. ``use`` selalu official — nilai lain ditolak IG."""
    return {"use": "official", "system": system, "value": value}


def administrative_code(slices: Iterable[Sequence[str]]) -> dict[str, Any]:
    """Extension administrativeCode dengan irisan bertingkat.

    SATUSEHAT memecah kode wilayah menjadi enam irisan; satu ``valueCode`` datar sah secara R4
    tetapi tidak terbaca sebagai wilayah.
    """
    return {
        "url": EXT_ADMINISTRATIVE_CODE,
        "extension": [{"url": nama, "valueCode": kode} for nama, kode in slices],
    }
