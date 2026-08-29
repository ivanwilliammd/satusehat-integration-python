from src.builder.base_builder import BaseBuilder

class SubstanceBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("Substance")

    def identifier(self, system: str, value: str) -> "SubstanceBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def status(self, value: str) -> "SubstanceBuilder":
        return self._set("status", value)

    def category(self, codeable_concept: dict) -> "SubstanceBuilder":
        return self._push("category", codeable_concept)

    def code(self, codeable_concept: dict) -> "SubstanceBuilder":
        return self._set("code", codeable_concept)

    def description(self, value: str) -> "SubstanceBuilder":
        return self._set("description", value)
