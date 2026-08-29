from src.builder.base_builder import BaseBuilder

class ChargeItemDefinitionBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("ChargeItemDefinition")

    def url(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self._set("url", value)

    def version(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self._set("version", value)

    def name(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self._set("name", value)

    def title(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self._set("title", value)

    def status(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self._set("status", value)

    def date(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self._set("date", value)

    def publisher(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self._set("publisher", value)

    def description(self, value: str) -> "ChargeItemDefinitionBuilder":
        return self._set("description", value)

    def code(self, codeable_concept: dict) -> "ChargeItemDefinitionBuilder":
        return self._set("code", codeable_concept)
