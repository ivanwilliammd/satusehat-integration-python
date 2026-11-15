"""ClaimResponse resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderClaimResponse.php. Versi sebelumnya menaruh adjudikasi di dalam
item (bentuk yang benar menurut R4) sementara PHP menumpuknya ke daftar `item`.
Karena kanon adalah PHP, port ini meniru PHP dan menandai cacatnya — kalau kanon
diperbaiki, ketiga port ikut berubah bersama golden-nya.
"""
from typing import Any, Dict, Optional

from src.builder.base_builder import BaseBuilder


def _kode(system: str, code: str, display: str = "") -> Dict[str, Any]:
    return {"coding": [{"system": system, "code": code, "display": display}]}


class ClaimResponseBuilder(BaseBuilder):
    """Builder for ClaimResponse resource."""

    def __init__(self):
        super().__init__("ClaimResponse")

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

    def _set_path(self, path: str, value: Any) -> "ClaimResponseBuilder":
        induk, kunci = self._titik(path)
        induk[kunci] = value
        return self

    def _push_path(self, path: str, value: Any) -> "ClaimResponseBuilder":
        induk, kunci = self._titik(path)
        if not isinstance(induk.get(kunci), list):
            induk[kunci] = []
        induk[kunci].append(value)
        return self

    def _push(self, key: str, value: Any) -> "ClaimResponseBuilder":  # type: ignore[override]
        self.data.setdefault(key, []).append(value)
        return self

    # --- setter ---------------------------------------------------------------

    def set_id(self, id: str) -> "ClaimResponseBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, system: str, value: str) -> "ClaimResponseBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_status(self, status: str) -> "ClaimResponseBuilder":
        self.data["status"] = status
        return self

    def set_type(self, system: str, code: str, display: str = "") -> "ClaimResponseBuilder":
        self.data["type"] = _kode(system, code, display)
        return self

    def set_sub_type(self, system: str, code: str, display: str = "") -> "ClaimResponseBuilder":
        self.data["subType"] = _kode(system, code, display)
        return self

    def set_use(self, use: str) -> "ClaimResponseBuilder":
        self.data["use"] = use
        return self

    def set_patient(self, reference: str) -> "ClaimResponseBuilder":
        self.data["patient"] = {"reference": reference}
        return self

    def set_created(self, created: str) -> "ClaimResponseBuilder":
        self.data["created"] = created
        return self

    def set_insurer(self, reference: str) -> "ClaimResponseBuilder":
        self.data["insurer"] = {"reference": reference}
        return self

    def set_requestor(self, reference: str) -> "ClaimResponseBuilder":
        self.data["requestor"] = {"reference": reference}
        return self

    def set_request(self, reference: str) -> "ClaimResponseBuilder":
        self.data["request"] = {"reference": reference}
        return self

    def set_outcome(self, outcome: str) -> "ClaimResponseBuilder":
        self.data["outcome"] = outcome
        return self

    def set_disposition(self, disposition: str) -> "ClaimResponseBuilder":
        self.data["disposition"] = disposition
        return self

    def set_pre_auth_ref(self, pre_auth_ref: str) -> "ClaimResponseBuilder":
        self.data["preAuthRef"] = pre_auth_ref
        return self

    def set_pre_auth_period(self, start: str, end: str = "") -> "ClaimResponseBuilder":
        self._set_path("preAuthPeriod/start", start)
        if end:
            self._set_path("preAuthPeriod/end", end)
        return self

    def set_payee_type(self, system: str, code: str, display: str = "") -> "ClaimResponseBuilder":
        self.data["payeeType"] = _kode(system, code, display)
        return self

    def add_item(
        self,
        item_sequence: int,
        detail_sequence: Optional[int] = None,
        sub_detail_sequence: Optional[int] = None,
    ) -> "ClaimResponseBuilder":
        item: Dict[str, Any] = {"itemSequence": item_sequence}
        if detail_sequence is not None:
            item["detailSequence"] = detail_sequence
        if sub_detail_sequence is not None:
            item["subDetailSequence"] = sub_detail_sequence
        return self._push("item", item)

    def add_item_adjudication(
        self,
        item_sequence: int,
        category_system: str,
        category_code: str,
        value: Optional[float] = None,
        reason_system: Optional[str] = None,
        reason_code: Optional[str] = None,
    ) -> "ClaimResponseBuilder":
        """Quirk PHP: menumpuk ke `item`, bukan ke `item[<i>]/adjudication`."""
        adjudication: Dict[str, Any] = {
            "itemSequence": item_sequence,
            "category": {"coding": [{"system": category_system, "code": category_code}]},
        }
        if value is not None:
            adjudication["value"] = value
        if reason_system and reason_code:
            adjudication["reason"] = {"coding": [{"system": reason_system, "code": reason_code}]}
        return self._push("item", adjudication)

    def add_add_item(
        self,
        item_sequence: int,
        product_or_service_system: str,
        product_or_service_code: str,
        product_or_service_display: Optional[str] = None,
    ) -> "ClaimResponseBuilder":
        return self._push(
            "addItem",
            {
                "itemSequence": [item_sequence],
                "productOrService": _kode(
                    product_or_service_system, product_or_service_code, product_or_service_display or ""
                ),
            },
        )

    def add_add_item_adjudication(
        self,
        sequence_link_id: int,
        category_system: str,
        category_code: str,
        value: Optional[float] = None,
    ) -> "ClaimResponseBuilder":
        """Menempel ke addItem TERAKHIR, seperti PHP (`count(...) - 1`)."""
        item_idx = len(self.data.get("addItem") or []) - 1
        adjudication: Dict[str, Any] = {
            "itemSequence": sequence_link_id,
            "category": {"coding": [{"system": category_system, "code": category_code}]},
        }
        if value is not None:
            adjudication["value"] = value
        return self._push_path(f"addItem/{item_idx}/adjudication", adjudication)

    def add_error(self, item_sequence: int, code_system: str, code: str, display: str = "") -> "ClaimResponseBuilder":
        return self._push(
            "error", {"itemSequence": item_sequence, "code": {"coding": [{"system": code_system, "code": code, "display": display}]}}
        )

    def add_coverage(
        self,
        sequence: int,
        reference: str,
        focal: Optional[bool] = None,
        priority_system: Optional[str] = None,
        priority_code: Optional[str] = None,
    ) -> "ClaimResponseBuilder":
        coverage: Dict[str, Any] = {"sequence": sequence, "reference": reference}
        if focal is not None:
            coverage["focal"] = bool(focal)
        if priority_system and priority_code:
            coverage["priority"] = {"coding": [{"system": priority_system, "code": priority_code}]}
        return self._push("coverage", coverage)

    def set_total(self, value: float, category_system: str, category_code: str) -> "ClaimResponseBuilder":
        """Dinamai set, tetapi MENUMPUK: ClaimResponse.total 0..*."""
        return self._push(
            "total", {"category": {"coding": [{"system": category_system, "code": category_code}]}, "value": value}
        )

    def set_payment(
        self,
        value: float,
        type_system: str,
        type_code: str,
        date: str,
        reference: Optional[str] = None,
    ) -> "ClaimResponseBuilder":
        self._set_path("payment/type", {"coding": [{"system": type_system, "code": type_code}]})
        self._set_path("payment/date", date)
        self._set_path("payment/amount/value", value)
        if reference:
            self._set_path("payment/reference", reference)
        return self

    # --- alias nama lama ------------------------------------------------------

    def add_decision_reason(self, system: str, code: str, display: Optional[str] = None) -> "ClaimResponseBuilder":
        reason: Dict[str, Any] = {"coding": [{"system": system, "code": code}]}
        if display:
            reason["coding"][0]["display"] = display
        return self._push("decisionReason", reason)

    def add_communication_request(self, reference: str) -> "ClaimResponseBuilder":
        return self._push("communicationRequest", {"reference": reference})

    def add_insurance(
        self,
        sequence: int,
        coverage_reference: str,
        focal: bool = False,
        coverage_display: Optional[str] = None,
    ) -> "ClaimResponseBuilder":
        insurance: Dict[str, Any] = {
            "sequence": sequence,
            "coverage": {"reference": coverage_reference},
            "focal": focal,
        }
        if coverage_display:
            insurance["coverage"]["display"] = coverage_display
        return self._push("insurance", insurance)
