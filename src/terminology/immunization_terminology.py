"""
Immunization terminology constants.

Ported from: Satusehat\Integration\Terminology\ImmunizationTerminology
Source: satusehat-integration (Laravel)

Contains vaccine product to terminology mappings (KFA -> CVX/SNOMED).
"""
from __future__ import annotations


class ImmunizationTerminology:
    """
    Static immunization terminology constants.
    Maps KFA product codes to CVX and SNOMED CT codes.

    Ported from Laravel static class ImmunizationTerminology.
    """

    # Maps KFA product code -> list of {system, code, display} mappings
    vaccine_map: dict[str, list[dict[str, str]]] = {
        "93001282": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93001282", "display": "Vaksin DTP-HB-Hib 0,5 mL (PENTABIO, 1)"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG17", "display": "HIB"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG45", "display": "HepB"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG107", "display": "DTAP"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "198", "display": "DTP-hepB-Hib Pentavalent Non-US"},
        ],
        "93003730": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93003730", "display": "Vaksin Hepatitis B Recombinant 20 ug/1 mL Suspensi Injeksi (Umum)"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG45", "display": "HepB"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "43", "display": "Hep B, adult"},
        ],
        "93005208": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93005208", "display": "Vaksin BCG Kering 0.375 mg/mL Serbuk Injeksi (BIO FARMA, 20)"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG19", "display": "BCG"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "19", "display": "BCG"},
        ],
        "93001283": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93001283", "display": "Vaksin DTP-HB-Hib 0,5 mL (PENTABIO, 5)"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG45", "display": "HepB"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "198", "display": "DTP-hepB-Hib Pentavalent Non-US"},
        ],
        "93004972": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93004972", "display": "Vaksin Poliomyelitis Oral Bivalent Tipe 1 & 3"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG89", "display": "POLIO"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "178", "display": "OPV bivalent"},
        ],
        "93004736": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93004736", "display": "Vaksin Poliomyelitis Inaktif (IPV) 0,5 mL (Shan IPV, 10)"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG89", "display": "POLIO"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "10", "display": "IPV"},
        ],
        "93005779": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93005779", "display": "Vaksin M/R 1000 CCID_50, 0.5 mL (BIO FARMA, 1)"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG03", "display": "MMR"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "4", "display": "M/R"},
        ],
        "93001619": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93001619", "display": "Vaksin Streptococcus Pneumoniae Serotype 0,5mL (PNEUMOSIL, 1)"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG152", "display": "PneumoPCV"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "152", "display": "Pneumococcal Conjugate, unspecified formulation"},
        ],
        "93001623": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93001623", "display": "Vaksin HPV quadrivalent 0,5 mL (GARDASIL, 1)"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG137", "display": "HPV"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "62", "display": "HPV, quadrivalent"},
        ],
        "93001589": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93001589", "display": "Vaksin Rabies (Wistar PM/WI 38-1503-3M Strain) 2,5 IU 0,5 mL (VERORAB)"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG90", "display": "RABIES"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "18", "display": "rabies, intramuscular injection"},
        ],
        "93001560": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93001560", "display": "Vaksin Yellow Fever 1000 IU 0,5 mL (STAMARIL PASTEUR, 1)"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG184", "display": "MENING"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "183", "display": "Yellow fever vaccine - alt"},
        ],
        "93001278": [
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "93001278", "display": "Vaksin Meningococcal Polysaccharide 50 ug 0,5 mL (MENIVAX ACYW)"},
            {"system": "http://sys-ids.kemkes.go.id/kfa", "code": "VG108", "display": "MENING"},
            {"system": "http://hl7.org/fhir/sid/cvx", "code": "108", "display": "meningococcal ACWY, unspecified formulation"},
        ],
    }
