from src.builder.base_builder import BaseBuilder

class FamilyMemberHistoryBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("FamilyMemberHistoryBuilder")

    def status(self, value: str) -> "FamilyMemberHistoryBuilder":
        return self._set("status", value)

    def patient(self, reference: str) -> "FamilyMemberHistoryBuilder":
        return self._set("patient", {"reference": reference})

    def relationship(self, codeable_concept: dict) -> "FamilyMemberHistoryBuilder":
        return self._set("relationship", codeable_concept)

    def code(self, codeable_concept: dict) -> "FamilyMemberHistoryBuilder":
        return self._set("code", codeable_concept)

    def date(self, value: str) -> "FamilyMemberHistoryBuilder":
        return self._set("date", value)

    def note(self, text: str) -> "FamilyMemberHistoryBuilder":
        return self._set("note", [{"text": text}])
