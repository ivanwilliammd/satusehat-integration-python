"""Claim resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderClaim.php. Versi sebelumnya memakai nama dan urutan argumen
yang berbeda dari PHP (`add_item(sequence, service_code, service_system)`,
`add_insurance(sequence, coverage_reference, ...)`), sehingga payload yang
dihasilkan tidak bisa dibandingkan dengan kanon. Ditulis ulang mengikuti PHP;
nama lama dipertahankan sebagai alias, kecuali `add_item`: urutan argumennya di
PHP adalah (system, code, display), jadi mengubahnya menjadi (code, system) akan
mengulangi cacat yang baru saja diperbaiki di 22 setter lain.

Tiga quirk PHP ditiru dan ditandai, bukan diperbaiki:
- add_item_quantity menulis `quantity/currency`, padahal Claim.item.quantity
  bertipe Quantity (value + unit);
- add_insurance_account menumpuk ke `insurance/account` tanpa kerangka insurance
  (sequence/focal/coverage);
- add_item_location menulis CodeableConcept, padahal item.location bertipe Address.
"""
from typing import Any, Dict, List, Optional

from satusehat_integration.builder.base_builder import BaseBuilder


def _kode(system: str, code: str, display: str = "") -> Dict[str, Any]:
    return {"coding": [{"system": system, "code": code, "display": display}]}


class ClaimBuilder(BaseBuilder):
    """Builder for Claim resource."""

    def __init__(self):
        super().__init__("Claim")

    # --- jalur bersarang ------------------------------------------------------

    @staticmethod
    def _is_index(seg: str) -> bool:
        return seg.isdigit()

    def _titik(self, path: str):
        segs = path.split("/")
        cur: Any = self.data
        for i, seg in enumerate(segs[:-1]):
            kunci: Any = int(seg) if self._is_index(seg) else seg
            if isinstance(cur, list):
                while len(cur) <= kunci:
                    cur.append({})
                cur = cur[kunci]
                continue
            if kunci not in cur or cur[kunci] is None:
                cur[kunci] = [] if self._is_index(segs[i + 1]) else {}
            cur = cur[kunci]
        terakhir = segs[-1]
        return cur, int(terakhir) if self._is_index(terakhir) else terakhir

    def _set_path(self, path: str, value: Any) -> "ClaimBuilder":
        induk, kunci = self._titik(path)
        induk[kunci] = value
        return self

    def _push_path(self, path: str, value: Any) -> "ClaimBuilder":
        induk, kunci = self._titik(path)
        if not isinstance(induk.get(kunci), list):
            induk[kunci] = []
        induk[kunci].append(value)
        return self

    def _push(self, key: str, value: Any) -> "ClaimBuilder":  # type: ignore[override]
        self.data.setdefault(key, []).append(value)
        return self

    # --- setter ---------------------------------------------------------------

    def set_id(self, id: str) -> "ClaimBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, system: str, value: str) -> "ClaimBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_status(self, status: str) -> "ClaimBuilder":
        self.data["status"] = status
        return self

    def set_type(self, system: str, code: str, display: str = "") -> "ClaimBuilder":
        self.data["type"] = _kode(system, code, display)
        return self

    def set_sub_type(self, system: str, code: str, display: str = "") -> "ClaimBuilder":
        self.data["subType"] = _kode(system, code, display)
        return self

    def set_use(self, use: str) -> "ClaimBuilder":
        self.data["use"] = use
        return self

    def set_priority(self, system: str, code: str, display: str = "") -> "ClaimBuilder":
        self.data["priority"] = _kode(system, code, display)
        return self

    def set_patient(self, reference: str, display: str = "") -> "ClaimBuilder":
        patient: Dict[str, Any] = {"reference": reference}
        if display:
            patient["display"] = display
        self.data["patient"] = patient
        return self

    def set_billable_period(self, start: str, end: str = "") -> "ClaimBuilder":
        self._set_path("billablePeriod/start", start)
        if end:
            self._set_path("billablePeriod/end", end)
        return self

    def set_created(self, created: str) -> "ClaimBuilder":
        self.data["created"] = created
        return self

    def set_enterer(self, reference: str) -> "ClaimBuilder":
        self.data["enterer"] = {"reference": reference}
        return self

    def set_insurer(self, reference: str) -> "ClaimBuilder":
        self.data["insurer"] = {"reference": reference}
        return self

    def set_provider(self, reference: str) -> "ClaimBuilder":
        self.data["provider"] = {"reference": reference}
        return self

    def set_priority_payor(self, reference: str) -> "ClaimBuilder":
        return self._push("priorityPayor", {"reference": reference})

    def set_prescriber(self, reference: str) -> "ClaimBuilder":
        self.data["prescriber"] = {"reference": reference}
        return self

    def set_facility(self, reference: str, display: str = "") -> "ClaimBuilder":
        facility: Dict[str, Any] = {"reference": reference}
        if display:
            facility["display"] = display
        self.data["facility"] = facility
        return self

    def add_related(
        self,
        reference_system: Optional[str] = None,
        reference_code: Optional[str] = None,
        reference_display: Optional[str] = None,
        relationship_system: Optional[str] = None,
        relationship_code: Optional[str] = None,
    ) -> "ClaimBuilder":
        related: Dict[str, Any] = {}
        if reference_system and reference_code:
            related["reference"] = {
                "system": reference_system,
                "code": reference_code,
                "display": reference_display or "",
            }
        if relationship_system and relationship_code:
            related["relationship"] = {"coding": [{"system": relationship_system, "code": relationship_code}]}
        return self._push("related", related)

    def add_coverage(
        self,
        reference: str,
        focal: Optional[bool] = None,
        priority_system: Optional[str] = None,
        priority_code: Optional[str] = None,
    ) -> "ClaimBuilder":
        coverage: Dict[str, Any] = {"reference": reference}
        if focal is not None:
            coverage["focal"] = bool(focal)
        if priority_system and priority_code:
            coverage["priority"] = {"coding": [{"system": priority_system, "code": priority_code}]}
        return self._push("coverage", coverage)

    def add_item(
        self,
        sequence: int,
        product_or_service_system: str,
        product_or_service_code: str,
        product_or_service_display: str,
        care_team_sequence: Optional[int] = None,
        diagnosis_sequence: Optional[int] = None,
        procedure_sequence: Optional[int] = None,
        information_sequence: Optional[int] = None,
    ) -> "ClaimBuilder":
        item: Dict[str, Any] = {
            "sequence": sequence,
            "productOrService": _kode(product_or_service_system, product_or_service_code, product_or_service_display),
        }
        if care_team_sequence is not None:
            item["careTeamSequence"] = [care_team_sequence]
        if diagnosis_sequence is not None:
            item["diagnosisSequence"] = [diagnosis_sequence]
        if procedure_sequence is not None:
            item["procedureSequence"] = [procedure_sequence]
        if information_sequence is not None:
            item["informationSequence"] = [information_sequence]
        return self._push("item", item)

    def add_item_serviced_period(self, item_idx: int, start: str, end: str = "") -> "ClaimBuilder":
        self._set_path(f"item/{item_idx}/servicedPeriod/start", start)
        if end:
            self._set_path(f"item/{item_idx}/servicedPeriod/end", end)
        return self

    def add_item_location(self, item_idx: int, system: str, code: str, display: str = "") -> "ClaimBuilder":
        """Quirk PHP: item.location di R4 bertipe Address, di sini ditulis CodeableConcept."""
        return self._push_path(f"item/{item_idx}/location", _kode(system, code, display))

    def add_item_quantity(self, item_idx: int, value: float, code: str = "IDR") -> "ClaimBuilder":
        """Quirk PHP: quantity/currency, padahal Claim.item.quantity bertipe Quantity."""
        self._set_path(f"item/{item_idx}/quantity/value", value)
        self._set_path(f"item/{item_idx}/quantity/currency", code)
        return self

    def add_item_unit_price(self, item_idx: int, value: float, code: str = "IDR") -> "ClaimBuilder":
        self._set_path(f"item/{item_idx}/unitPrice/value", value)
        self._set_path(f"item/{item_idx}/unitPrice/currency", code)
        return self

    def add_care_team(
        self,
        sequence: int,
        provider_reference: str,
        role_system: Optional[str] = None,
        role_code: Optional[str] = None,
        role_display: Optional[str] = None,
    ) -> "ClaimBuilder":
        care_team: Dict[str, Any] = {"sequence": sequence, "provider": {"reference": provider_reference}}
        if role_system and role_code:
            care_team["role"] = {
                "coding": [{"system": role_system, "code": role_code, "display": role_display or ""}]
            }
        return self._push("careTeam", care_team)

    def add_diagnosis(
        self,
        sequence: int,
        system: str,
        code: str,
        type_system: Optional[str] = None,
        type_code: Optional[str] = None,
    ) -> "ClaimBuilder":
        diagnosis: Dict[str, Any] = {
            "sequence": sequence,
            "diagnosisCodeableConcept": {"coding": [{"system": system, "code": code}]},
        }
        if type_system and type_code:
            diagnosis["type"] = {"coding": [{"system": type_system, "code": type_code}]}
        return self._push("diagnosis", diagnosis)

    def add_procedure(
        self,
        sequence: int,
        system: str,
        code: str,
        date: Optional[str] = None,
        type_system: Optional[str] = None,
        type_code: Optional[str] = None,
    ) -> "ClaimBuilder":
        procedure: Dict[str, Any] = {
            "sequence": sequence,
            "procedureCodeableConcept": {"coding": [{"system": system, "code": code}]},
        }
        if date:
            procedure["date"] = date
        if type_system and type_code:
            procedure["type"] = {"coding": [{"system": type_system, "code": type_code}]}
        return self._push("procedure", procedure)

    def add_insurance_account(self, reference: str) -> "ClaimBuilder":
        """Quirk PHP: menumpuk ke insurance/account tanpa kerangka insurance."""
        return self._push_path("insurance/account", {"reference": reference})

    def set_total(self, value: float, code: str = "IDR") -> "ClaimBuilder":
        self.data["total"] = {"value": value, "currency": code}
        return self

    # --- alias nama lama ------------------------------------------------------

    def set_priority_code(self, system: str = "http://hl7.org/fhir/request-priority", code: str = "") -> "ClaimBuilder":
        return self.set_priority(system, code)

    def add_supporting_info(self, sequence: int, code: str, code_system: str, value: Optional[str] = None) -> "ClaimBuilder":
        info: Dict[str, Any] = {"sequence": sequence, "category": {"coding": [{"system": code_system, "code": code}]}}
        if value:
            info["valueString"] = value
        return self._push("supportingInfo", info)

    def add_insurance(
        self,
        sequence: int,
        coverage_reference: str,
        focal: bool = False,
        coverage_display: Optional[str] = None,
    ) -> "ClaimBuilder":
        insurance: Dict[str, Any] = {
            "sequence": sequence,
            "coverage": {"reference": coverage_reference},
            "focal": focal,
        }
        if coverage_display:
            insurance["coverage"]["display"] = coverage_display
        return self._push("insurance", insurance)

    def add_item_encounter(self, item_index: int, encounter_reference: str) -> "ClaimBuilder":
        return self._push_path(f"item/{item_index}/encounter", {"reference": encounter_reference})
