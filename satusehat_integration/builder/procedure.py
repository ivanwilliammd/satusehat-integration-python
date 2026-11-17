"""Procedure FHIR R4 resource builder.

Cermin dari PayloadBuilderProcedure pada SDK PHP, ditambah bentuk API lama Python
(set_reporter, add_complication, set_location) yang tetap dipertahankan.
"""

from typing import Any, Dict, Optional

from satusehat_integration.builder.base_builder import BaseBuilder


def _arr(value: Any) -> Any:
    return value.to_array() if hasattr(value, "to_array") else value


def _coding(code: Any, display: Optional[str], system: str) -> Dict[str, Any]:
    """Terima objek/dict CodeableConcept, atau (code, display, system)."""
    if isinstance(code, str):
        return {"coding": [{"system": system, "code": code, "display": display or code}]}
    return _arr(code)


class ProcedureBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Procedure")

    def set_id(self, id: str) -> "ProcedureBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "ProcedureBuilder":
        if value is not None:
            return self._push("identifier", {"system": identifier, "value": value})
        return self._push("identifier", _arr(identifier))

    def set_status(self, status: str) -> "ProcedureBuilder":
        self.data["status"] = status
        return self

    def set_category(self, category: Any, display: Optional[str] = None, system: str = "http://snomed.info/sct") -> "ProcedureBuilder":
        self.data["category"] = _coding(category, display, system)
        return self

    def set_code(self, code: Any, display: Optional[str] = None, system: str = "http://snomed.info/sct") -> "ProcedureBuilder":
        self.data["code"] = _coding(code, display, system)
        return self

    def set_subject(self, subject: Any, display: Optional[str] = None) -> "ProcedureBuilder":
        if isinstance(subject, str):
            subj: Dict[str, Any] = {"reference": subject}
            if display:
                subj["display"] = display
            self.data["subject"] = subj
        else:
            self.data["subject"] = _arr(subject)
        return self

    def set_encounter(self, encounter: Any, display: Optional[str] = None) -> "ProcedureBuilder":
        if isinstance(encounter, str):
            enc: Dict[str, Any] = {"reference": encounter}
            if display:
                enc["display"] = display
            self.data["encounter"] = enc
        else:
            self.data["encounter"] = _arr(encounter)
        return self

    def add_based_on(self, based_on: Any) -> "ProcedureBuilder":
        return self._push("basedOn", _arr(based_on))

    def add_reason_code(self, reason_code: Any) -> "ProcedureBuilder":
        return self._push("reasonCode", _arr(reason_code))

    def add_reason(self, code: str, display: str, system: str = "http://snomed.info/sct") -> "ProcedureBuilder":
        return self._push("reasonCode", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_performed_date_time(self, date_time: str) -> "ProcedureBuilder":
        self.data["performedDateTime"] = date_time
        return self

    def set_performed(self, performed: str) -> "ProcedureBuilder":
        """Alias lama untuk performedDateTime."""
        return self.set_performed_date_time(performed)

    def set_performed_period(self, period: Any, end: Optional[str] = None) -> "ProcedureBuilder":
        if isinstance(period, str):
            self.data["performedPeriod"] = {"start": period, "end": end}
        else:
            self.data["performedPeriod"] = _arr(period)
        return self

    def set_performed_string(self, performed_string: str) -> "ProcedureBuilder":
        self.data["performedString"] = performed_string
        return self

    def set_performed_age(self, age: Any) -> "ProcedureBuilder":
        self.data["performedAge"] = _arr(age)
        return self

    def set_performed_range(self, performed_range: Any) -> "ProcedureBuilder":
        self.data["performedRange"] = _arr(performed_range)
        return self

    def add_performer(
        self,
        actor: Any,
        display: Optional[str] = None,
        function_code: Optional[str] = None,
        function_display: Optional[str] = None,
        on_behalf_of: Any = None,
    ) -> "ProcedureBuilder":
        # FHIR R4: Procedure.performer.actor. Versi lama menulis "individual" — sudah tidak dipakai.
        if isinstance(actor, str):
            entry: Dict[str, Any] = {"actor": {"reference": actor}}
            if display:
                entry["actor"]["display"] = display
        else:
            entry = {"actor": _arr(actor)}
        if function_code:
            entry["function"] = {
                "coding": [{"code": function_code, "display": function_display or function_code}]
            }
        if on_behalf_of is not None:
            entry["onBehalfOf"] = _arr(on_behalf_of)
        return self._push("performer", entry)

    def set_reporter(self, reporter: Any, display: Optional[str] = None) -> "ProcedureBuilder":
        if isinstance(reporter, str):
            rep: Dict[str, Any] = {"reference": reporter}
            if display:
                rep["display"] = display
            self.data["reporter"] = rep
        else:
            self.data["reporter"] = _arr(reporter)
        return self

    def set_location(self, location: Any, display: Optional[str] = None) -> "ProcedureBuilder":
        if isinstance(location, str):
            loc: Dict[str, Any] = {"reference": location}
            if display:
                loc["display"] = display
            self.data["location"] = loc
        else:
            self.data["location"] = _arr(location)
        return self

    def set_outcome(self, outcome: Any, display: Optional[str] = None) -> "ProcedureBuilder":
        self.data["outcome"] = _coding(outcome, display, "http://snomed.info/sct")
        return self

    def add_report(self, report: Any) -> "ProcedureBuilder":
        return self._push("report", _arr(report))

    def add_follow_up(self, follow_up: Any) -> "ProcedureBuilder":
        return self._push("followUp", _arr(follow_up))

    def add_note(self, note: Any) -> "ProcedureBuilder":
        return self._push("note", {"text": note} if isinstance(note, str) else _arr(note))

    def add_focal_device(
        self, action: Any, device: Any = None, manufacture_item: Any = None
    ) -> "ProcedureBuilder":
        row: Dict[str, Any] = {"action": _arr(action)}
        if device is not None:
            row["device"] = _arr(device)
        if manufacture_item is not None:
            row["manufactureItem"] = _arr(manufacture_item)
        return self._push("focalDevice", row)

    def add_used_reference(self, reference: Any, type_: Any = None) -> "ProcedureBuilder":
        row: Dict[str, Any] = dict(_arr(reference))
        if type_ is not None:
            row["type"] = _arr(type_)
        return self._push("usedReference", row)

    def add_used_code(self, used_code: Any) -> "ProcedureBuilder":
        return self._push("usedCode", _arr(used_code))

    def add_body_site(self, body_site: Any, display: Optional[str] = None, system: str = "http://snomed.info/sct") -> "ProcedureBuilder":
        return self._push("bodySite", _coding(body_site, display, system))

    def add_complication(self, code: str, display: str, system: str = "http://snomed.info/sct") -> "ProcedureBuilder":
        return self._push("complication", {"coding": [{"system": system, "code": code, "display": display}]})

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "ProcedureBuilder":
        extension: Dict[str, Any] = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        return self._push("extension", extension)
