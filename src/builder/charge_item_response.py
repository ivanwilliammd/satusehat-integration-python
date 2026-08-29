from src.builder.base_builder import BaseBuilder

class ChargeItemResponseBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ChargeItemResponseBuilder")

    def status(self, value: str) -> "ChargeItemResponseBuilder":
        return self._set("status", value)

    def charge_item(self, reference: str) -> "ChargeItemResponseBuilder":
        return self._set("chargeItem", {"reference": reference})

    def request(self, reference: str) -> "ChargeItemResponseBuilder":
        return self._set("request", {"reference": reference})

    def outcome(self, codeable_concept: dict) -> "ChargeItemResponseBuilder":
        return self._set("outcome", codeable_concept)

    def description(self, value: str) -> "ChargeItemResponseBuilder":
        return self._set("description", value)

    def created(self, value: str) -> "ChargeItemResponseBuilder":
        return self._set("created", value)

    def requestor(self, reference: str) -> "ChargeItemResponseBuilder":
        return self._set("requestor", {"reference": reference})
