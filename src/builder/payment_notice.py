from src.builder.base_builder import BaseBuilder

class PaymentNoticeBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("PaymentNotice")

    def status(self, value: str) -> "PaymentNoticeBuilder":
        return self._set("status", value)

    def request(self, reference: str) -> "PaymentNoticeBuilder":
        return self._set("request", {"reference": reference})

    def response(self, reference: str) -> "PaymentNoticeBuilder":
        return self._set("response", {"reference": reference})

    def created(self, value: str) -> "PaymentNoticeBuilder":
        return self._set("created", value)

    def provider(self, reference: str) -> "PaymentNoticeBuilder":
        return self._set("provider", {"reference": reference})

    def amount(self, amount: dict) -> "PaymentNoticeBuilder":
        return self._set("amount", amount)
