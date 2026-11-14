from typing import Any, Dict, List, Optional

from src.builder.base_builder import BaseBuilder


class DiagnosticReportBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("DiagnosticReport")

    def add_identifier(self, system: str, value: str) -> "DiagnosticReportBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append({"system": system, "value": value})
        return self

    def set_status(self, status: str) -> "DiagnosticReportBuilder":
        self.data["status"] = status
        return self

    def add_category(
        self,
        code: Any,
        display: Optional[str] = None,
        system: str = "http://terminology.hl7.org/CodeSystem/v2-0074",
    ) -> "DiagnosticReportBuilder":
        if not isinstance(code, str):
            entry = code.to_array() if hasattr(code, "to_array") else code
            self.data.setdefault("category", []).append(entry)
            return self
        if "category" not in self.data:
            self.data["category"] = []
        self.data["category"].append({
            "coding": [{"system": system, "code": code, "display": display}]
        })
        return self

    def set_code(
        self,
        code: Any,
        display: Optional[str] = None,
        system: str = "http://loinc.org",
    ) -> "DiagnosticReportBuilder":
        if not isinstance(code, str):
            self.data["code"] = code.to_array() if hasattr(code, "to_array") else code
            return self
        self.data["code"] = {
            "coding": [{"system": system, "code": code, "display": display}]
        }
        return self

    def set_subject(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "DiagnosticReportBuilder":
        subj: Dict[str, Any] = {"reference": reference}
        if display:
            subj["display"] = display
        self.data["subject"] = subj
        return self

    def set_encounter(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "DiagnosticReportBuilder":
        enc: Dict[str, Any] = {"reference": reference}
        if display:
            enc["display"] = display
        self.data["encounter"] = enc
        return self

    def set_effective_time(self, effective_time: str) -> "DiagnosticReportBuilder":
        self.data["effectiveTime"] = effective_time
        return self

    def set_issued(self, issued: str) -> "DiagnosticReportBuilder":
        self.data["issued"] = issued
        return self

    def add_performer(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "DiagnosticReportBuilder":
        if "performer" not in self.data:
            self.data["performer"] = []
        perf: Dict[str, Any] = {"reference": reference}
        if display:
            perf["display"] = display
        self.data["performer"].append(perf)
        return self

    def add_result(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "DiagnosticReportBuilder":
        if "result" not in self.data:
            self.data["result"] = []
        res: Dict[str, Any] = {"reference": reference}
        if display:
            res["display"] = display
        self.data["result"].append(res)
        return self

    def set_conclusion(self, conclusion: str) -> "DiagnosticReportBuilder":
        self.data["conclusion"] = conclusion
        return self

    def set_formatted_text(self, formatted_text: str) -> "DiagnosticReportBuilder":
        self.data["text"] = {
            "status": "generated",
            "div": f"<div>{formatted_text}</div>"
        }
        return self

    # --- Nama kanon (cermin PayloadBuilderDiagnosticReport) ---

    def set_id(self, id: str) -> "DiagnosticReportBuilder":
        self.data["id"] = id
        return self

    def set_effective_date_time(self, date_time: str) -> "DiagnosticReportBuilder":
        self.data["effectiveDateTime"] = date_time
        return self

    def add_specimen(self, specimen: Any) -> "DiagnosticReportBuilder":
        entry = {"reference": specimen} if isinstance(specimen, str) else (
            specimen.to_array() if hasattr(specimen, "to_array") else specimen
        )
        self.data.setdefault("specimen", []).append(entry)
        return self

    def add_conclusion_code(self, conclusion_code: Any) -> "DiagnosticReportBuilder":
        entry = conclusion_code.to_array() if hasattr(conclusion_code, "to_array") else conclusion_code
        self.data.setdefault("conclusionCode", []).append(entry)
        return self

    def add_based_on(self, based_on: Any) -> "DiagnosticReportBuilder":
        entry = {"reference": based_on} if isinstance(based_on, str) else (
            based_on.to_array() if hasattr(based_on, "to_array") else based_on
        )
        self.data.setdefault("basedOn", []).append(entry)
        return self

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "DiagnosticReportBuilder":
        extension: Dict[str, Any] = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        self.data.setdefault("extension", []).append(extension)
        return self
