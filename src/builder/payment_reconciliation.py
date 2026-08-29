from src.builder.base_builder import BaseBuilder

class PaymentReconciliationBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("PaymentReconciliation")

    def status(self, value: str) -> "PaymentReconciliationBuilder":
        return self._set("status", value)

    def created(self, value: str) -> "PaymentReconciliationBuilder":
        return self._set("created", value)

    def period_start(self, value: str) -> "PaymentReconciliationBuilder":
        return self._set("period", {"start": value})

    def period_end(self, value: str) -> "PaymentReconciliationBuilder":
        return self._set("periodEnd", value)

    def requestor(self, reference: str) -> "PaymentReconciliationBuilder":
        return self._set("requestor", {"reference": reference})

    def outcome(self, value: str) -> "PaymentReconciliationBuilder":
        return self._set("outcome", value)
