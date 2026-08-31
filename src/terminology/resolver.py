"""Terminology Resolver — casts strings, arrays, and CodeableConcept dicts to CodeableConcept format."""

SYSTEM_MAP = {
    "ICD10": "http://hl7.org/fhir/sid/icd-10",
    "ICD9": "http://hl7.org/fhir/sid/icd-9-cm",
    "ICD9CM": "http://hl7.org/fhir/sid/icd-9-cm",
    "LOINC": "http://loinc.org",
    "SNOMED": "http://snomed.info/sct",
    "CVX": "http://hl7.org/fhir/sid/cvx",
    "UCUM": "http://unitsofmeasure.org",
    "KFA": "http://fhir.kemkes.go.id/kfa",
    "KPTL": "http://fhir.kemkes.go.id/kptl",
    "RXNORM": "http://www.nlm.nih.gov/research/umls/rxnorm",
    "ICDO": "http://hl7.org/fhir/sid/icd-o",
    "ICDMM": "http://example.com/icd-mm",
    "ICDPM": "http://example.com/icd-pm",
    "MTI": "http://terminology.kemkes.go.id",
}


def resolve(value) -> dict:
    """
    Resolve a value to FHIR CodeableConcept format.

    Supports:
      - str "ICD10:A00"    → {coding: [{system, code, display}], text}
      - str "A00" (bare)   → {text: "A00"}
      - dict cc             → pass through
      - list of above       → list of resolved
    """
    if isinstance(value, list):
        return [resolve(v) for v in value]
    if isinstance(value, dict):
        return value  # pass through CodeableConcept dict
    if not isinstance(value, str):
        return {"text": str(value)}

    colon_idx = value.find(":")
    if colon_idx != -1:
        prefix = value[:colon_idx].upper()
        code = value[colon_idx + 1:].strip()
        system = SYSTEM_MAP.get(prefix, prefix)
        return {
            "coding": [{"system": system, "code": code, "display": code}],
            "text": code,
        }

    return {"text": value}


def expand_array(codes: list) -> list:
    """Expand a shorthand array into resolved CodeableConcept array."""
    return [resolve(code) for code in codes]


def is_valid(code: str, system: str = None) -> bool:
    """Validate a code against known terminology systems."""
    if not code or not code.strip():
        return False
    if system:
        return system.upper() in SYSTEM_MAP
    return True
