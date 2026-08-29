from src.builder.base_builder import BaseBuilder

class GenomicStudyBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("GenomicStudyBuilder")

    def status(self, value: str) -> "GenomicStudyBuilder":
        return self._set("status", value)

    def type(self, codeable_concept: dict) -> "GenomicStudyBuilder":
        return self._set("type", codeable_concept)

    def subject(self, reference: str) -> "GenomicStudyBuilder":
        return self._set("subject", {"reference": reference})

    def encounter(self, reference: str) -> "GenomicStudyBuilder":
        return self._set("encounter", {"reference": reference})

    def started(self, value: str) -> "GenomicStudyBuilder":
        return self._set("started", value)

    def based_on(self, reference: str) -> "GenomicStudyBuilder":
        return self._push("basedOn", {"reference": reference})
