"""Coverage FHIR R4 resource builder.

Cermin dari PayloadBuilderCoverage pada SDK PHP. Bentuk payload diuji terhadap golden yang sama
dipakai port Go dan Node.
"""

from typing import Dict, Optional

from satusehat_integration.builder.base_builder import BaseBuilder


class CoverageBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("Coverage")

    def set_id(self, id: str) -> "CoverageBuilder":
        return self._set("id", id)

    def add_identifier(self, system: str, value: str) -> "CoverageBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_status(self, status: str) -> "CoverageBuilder":
        return self._set("status", status)

    def set_type(self, system: str, code: str, display: str = "") -> "CoverageBuilder":
        # PHP selalu menulis display, termasuk string kosong.
        return self._set("type", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_policy_holder(self, reference: str) -> "CoverageBuilder":
        return self._set("policyHolder", {"reference": reference})

    def set_subscriber(self, reference: str) -> "CoverageBuilder":
        return self._set("subscriber", {"reference": reference})

    def set_subscriber_id(self, value: str) -> "CoverageBuilder":
        return self._set("subscriberId", value)

    def set_beneficiary(self, reference: str) -> "CoverageBuilder":
        return self._set("beneficiary", {"reference": reference})

    def set_dependent(self, value: str) -> "CoverageBuilder":
        return self._set("dependent", value)

    def set_relationship(self, system: str, code: str) -> "CoverageBuilder":
        return self._set("relationship", {"coding": [{"system": system, "code": code}]})

    def add_payor(self, reference: str, display: str = "") -> "CoverageBuilder":
        payor: Dict[str, str] = {"reference": reference}
        if display:
            payor["display"] = display
        return self._push("payor", payor)

    def set_class(self, type_system: str, type_code: str, value: str, name: str = "") -> "CoverageBuilder":
        row: Dict[str, object] = {
            "type": {"coding": [{"system": type_system, "code": type_code}]},
            "value": value,
        }
        if name:
            row["name"] = name
        return self._push("class", row)

    def set_order(self, order: int) -> "CoverageBuilder":
        return self._set("order", order)

    def set_network(self, network: str) -> "CoverageBuilder":
        return self._set("network", network)

    def set_cost_to_beneficiary(self, value: float, code: str = "IDR") -> "CoverageBuilder":
        # FHIR R4: costToBeneficiary.value[x] adalah Money.
        return self._push("costToBeneficiary", {"valueMoney": {"value": value, "currency": code}})

    def set_period(self, start: str, end: str = "") -> "CoverageBuilder":
        self._set("period/start", start)
        if end:
            self._set("period/end", end)
        return self
