from src.builder.base_builder import BaseBuilder

class QuestionnaireResponseBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("QuestionnaireResponseBuilder")

    def status(self, value: str) -> "QuestionnaireResponseBuilder":
        return self._set("status", value)

    def questionnaire(self, reference: str) -> "QuestionnaireResponseBuilder":
        return self._set("questionnaire", {"reference": reference})

    def subject(self, reference: str) -> "QuestionnaireResponseBuilder":
        return self._set("subject", {"reference": reference})

    def encounter(self, reference: str) -> "QuestionnaireResponseBuilder":
        return self._set("encounter", {"reference": reference})

    def authored(self, value: str) -> "QuestionnaireResponseBuilder":
        return self._set("authored", value)

    def author(self, reference: str) -> "QuestionnaireResponseBuilder":
        return self._set("author", {"reference": reference})
