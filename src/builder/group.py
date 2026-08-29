from src.builder.base_builder import BaseBuilder

class GroupBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("Group")

    def type(self, value: str) -> "GroupBuilder":
        return self._set("type", value)

    def active(self, value: bool) -> "GroupBuilder":
        return self._set("active", value)

    def name(self, value: str) -> "GroupBuilder":
        return self._set("name", value)

    def quantity(self, value: int) -> "GroupBuilder":
        return self._set("quantity", value)

    def member_entity(self, reference: str) -> "GroupBuilder":
        return self._push("member", {"entity": {"reference": reference}})
