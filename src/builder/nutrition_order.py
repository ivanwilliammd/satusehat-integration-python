from src.builder.base_builder import BaseBuilder

class NutritionOrderBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("NutritionOrderBuilder")

    def status(self, value: str) -> "NutritionOrderBuilder":
        return self._set("status", value)

    def intent(self, value: str) -> "NutritionOrderBuilder":
        return self._set("intent", value)

    def patient(self, reference: str) -> "NutritionOrderBuilder":
        return self._set("patient", {"reference": reference})

    def date_time(self, value: str) -> "NutritionOrderBuilder":
        return self._set("dateTime", value)

    def orderer(self, reference: str) -> "NutritionOrderBuilder":
        return self._set("orderer", {"reference": reference})
