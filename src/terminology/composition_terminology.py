"""
Composition terminology constants.

Ported from: Satusehat\Integration\Terminology\CompositionTerminology
Source: satusehat-integration (Laravel)

Contains LOINC and Kemkes composition type/category/section codes.
"""
from __future__ import annotations


class CompositionTerminology:
    """
    Static composition terminology for FHIR DocumentReference and Composition.

    Ported from Laravel static class CompositionTerminology.
    """

    # Composition type codes: code -> {system, display}
    type: dict[str, dict[str, str]] = {
        "18842-5": {"system": "http://loinc.org", "display": "Discharge summary"},
        "COM000001": {
            "system": "http://terminology.kemkes.go.id/CodeSystem/composition-type",
            "display": "Formulir Informasi Kematian Maternal",
        },
    }

    # Composition category codes: code -> {system, display}
    category: dict[str, dict[str, str]] = {
        "11369-6": {"system": "http://loinc.org", "display": "History of Immunization"},
        "11488-4": {"system": "http://loinc.org", "display": "Consult Note"},
        "11506-3": {"system": "http://loinc.org", "display": "Provider-unspecified progress note"},
        "18748-4": {"system": "http://loinc.org", "display": "Diagnostic imaging study"},
        "18776-5": {"system": "http://loinc.org", "display": "Plan of treatment (narrative)"},
        "18842-5": {"system": "http://loinc.org", "display": "Discharge summary"},
        "26436-6": {"system": "http://loinc.org", "display": "Laboratory Studies (set)"},
        "26441-6": {"system": "http://loinc.org", "display": "Cardiology studies (set)"},
        "28570-0": {"system": "http://loinc.org", "display": "Provider-unspecified procedure note"},
        "34109-9": {"system": "http://loinc.org", "display": "Evaluation and management note"},
        "34117-2": {"system": "http://loinc.org", "display": "Provider-unspecified, History and physical note"},
        "34121-4": {"system": "http://loinc.org", "display": "Interventional procedure note"},
        "34140-4": {"system": "http://loinc.org", "display": "Transfer of care referral note"},
        "42349-1": {"system": "http://loinc.org", "display": "Reason for referral (narrative)"},
        "46264-8": {"system": "http://loinc.org", "display": "History of medical device use"},
        "48765-2": {"system": "http://loinc.org", "display": "Allergies and adverse reactions Document"},
        "51848-0": {"system": "http://loinc.org", "display": "Evaluation note"},
        "57016-8": {"system": "http://loinc.org", "display": "Privacy Policy Acknowledgment Document"},
        "57133-1": {"system": "http://loinc.org", "display": "Referral note"},
        "LP173392-4": {"system": "http://loinc.org", "display": "Death certificate"},
        "LP181204-1": {"system": "http://loinc.org", "display": "Prescription"},
        "LP181529-1": {"system": "http://loinc.org", "display": "Prescription for diagnostic or specialist care"},
    }

    # Composition section codes: code -> {system, display}
    section: dict[str, dict[str, str]] = {
        "10154-3": {"system": "http://loinc.org", "display": "Chief complaint Narrative - Reported"},
        "10157-6": {"system": "http://loinc.org", "display": "History of family member diseases Narrative"},
        "10160-0": {"system": "http://loinc.org", "display": "History of medication use Narrative"},
        "10164-2": {"system": "http://loinc.org", "display": "History of present illness Narrative"},
        "11329-0": {"system": "http://loinc.org", "display": "History general Narrative - Reported"},
        "11348-0": {"system": "http://loinc.org", "display": "History of past illness Narrative"},
        "11369-6": {"system": "http://loinc.org", "display": "History of immunization Narrative"},
        "29549-3": {"system": "http://loinc.org", "display": "Medication administered Narrative"},
        "29554-3": {"system": "http://loinc.org", "display": "Procedure Narrative"},
        "29762-2": {"system": "http://loinc.org", "display": "Social history Narrative"},
        "30954-2": {"system": "http://loinc.org", "display": "Relevant diagnostic tests/laboratory data Narrative"},
        "42348-3": {"system": "http://loinc.org", "display": "Advance directives (narrative)"},
        "48765-2": {"system": "http://loinc.org", "display": "Allergies and adverse reactions Document"},
        "8716-3": {"system": "http://loinc.org", "display": "Vital signs"},
        "COS000001": {
            "system": "http://terminology.kemkes.go.id/CodeSystem/composition-section",
            "display": "Keadaan Saat Masuk",
        },
        "COS000004": {
            "system": "http://terminology.kemkes.go.id/CodeSystem/composition-section",
            "display": "Hasil Pemeriksaan Laboratorium",
        },
        "COS000005": {
            "system": "http://terminology.kemkes.go.id/CodeSystem/composition-section",
            "display": "Form Keluar",
        },
        "COS000009": {
            "system": "http://terminology.kemkes.go.id/CodeSystem/composition-section",
            "display": "Deteksi Dini Diabetes Melitus",
        },
        "TK000003": {
            "system": "http://terminology.kemkes.go.id",
            "display": "Anamnesis",
        },
        "TK000004": {
            "system": "http://terminology.kemkes.go.id",
            "display": "Diagnosis",
        },
        "TK000005": {
            "system": "http://terminology.kemkes.go.id",
            "display": "Tindakan/Prosedur Medis",
        },
        "TK000007": {
            "system": "http://terminology.kemkes.go.id",
            "display": "Pemeriksaan Fisik",
        },
        "TK000009": {
            "system": "http://terminology.kemkes.go.id",
            "display": "Hasil Pemeriksaan Penunjang",
        },
        "TK000013": {
            "system": "http://terminology.kemkes.go.id",
            "display": "Obat",
        },
    }
