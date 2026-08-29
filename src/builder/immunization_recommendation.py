from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class ImmunizationRecommendationBuilder(BaseBuilder):
    _resourceType = "ImmunizationRecommendation"

    def __init__(self) -> None:
        super().__init__("ImmunizationRecommendationBuilder")

    def subject(self, reference: str, display: Optional[str] = None) -> "ImmunizationRecommendationBuilder":
        sub: dict = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("subject", sub)

    def date(self, value: str) -> "ImmunizationRecommendationBuilder":
        return self._set("date", value)

    def authority(self, reference: str, display: Optional[str] = None) -> "ImmunizationRecommendationBuilder":
        auth: dict = {"reference": reference}
        if display:
            auth["display"] = display
        return self._set("authority", auth)

    def recommendation(self, vaccine_code: dict, target_disease: Optional[dict] = None, forecast_status: Optional[dict] = None, date_criterion: Optional[List[dict]] = None, description: Optional[str] = None, dose_quantity: Optional[dict] = None, series: Optional[str] = None, series_doses: Optional[int] = None, supporting_patient_info: Optional[List[str]] = None, supporting_immunization: Optional[List[str]] = None) -> "ImmunizationRecommendationBuilder":
        rec: dict = {"vaccineCode": vaccine_code}
        if target_disease:
            rec["targetDisease"] = target_disease
        if forecast_status:
            rec["forecastStatus"] = forecast_status
        if date_criterion:
            rec["dateCriterion"] = date_criterion
        if description:
            rec["description"] = description
        if dose_quantity:
            rec["doseQuantity"] = dose_quantity
        if series:
            rec["series"] = series
        if series_doses is not None:
            rec["seriesDoses"] = series_doses
        if supporting_patient_info:
            rec["supportingPatientInformation"] = [{"reference": r} for r in supporting_patient_info]
        if supporting_immunization:
            rec["supportingImmunization"] = [{"reference": r} for r in supporting_immunization]
        return self._append("recommendation", rec)
