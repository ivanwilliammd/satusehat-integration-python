from typing import Any, Dict, List, Optional, Union

from src.builder.base_builder import BaseBuilder


class RelatedPersonBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("RelatedPerson")

    def set_id(self, value: str) -> "RelatedPersonBuilder":
        return self._set("id", value)

    def add_identifier(self, identifier: Union[str, Dict[str, Any]], value: Optional[str] = None) -> "RelatedPersonBuilder":
        if isinstance(identifier, str):
            return self._push("identifier", {"system": identifier, "value": value})
        return self._push("identifier", identifier)

    def set_active(self, value: bool) -> "RelatedPersonBuilder":
        return self._set("active", value)

    def set_patient(self, patient: Union[Dict[str, Any], str], display: Optional[str] = None) -> "RelatedPersonBuilder":
        if isinstance(patient, str):
            ref = self._auto_prefix(patient, "Patient")
            result: Dict[str, Any] = {"reference": ref}
            if display:
                result["display"] = display
            return self._set("patient", result)
        return self._set("patient", patient)

    def add_relationship(self, relationship: Union[Dict[str, Any], str], display: Optional[str] = None) -> "RelatedPersonBuilder":
        if isinstance(relationship, str):
            cc: Dict[str, Any] = {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
                    "code": relationship,
                    "display": display or relationship,
                }]
            }
            return self._push("relationship", cc)
        return self._push("relationship", relationship)

    def add_name(self, name: Union[Dict[str, Any], str], text: Optional[str] = None) -> "RelatedPersonBuilder":
        if isinstance(name, str):
            return self._push("name", {"text": text or name})
        return self._push("name", name)

    def add_telecom(self, telecom: Union[Dict[str, Any], str], value: Optional[str] = None, use: str = "home") -> "RelatedPersonBuilder":
        if isinstance(telecom, str):
            return self._push("telecom", {"system": telecom, "value": value, "use": use})
        return self._push("telecom", telecom)

    def set_gender(self, value: str) -> "RelatedPersonBuilder":
        return self._set("gender", value)

    def set_birth_date(self, value: str) -> "RelatedPersonBuilder":
        return self._set("birthDate", value)

    def add_address(self, address: Union[Dict[str, Any], str]) -> "RelatedPersonBuilder":
        if isinstance(address, str):
            return self._push("address", {"text": address})
        return self._push("address", address)

    def add_communication(self, language: Union[Dict[str, Any], str], preferred: bool = True) -> "RelatedPersonBuilder":
        if isinstance(language, str):
            cc: Dict[str, Any] = {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v3-Language",
                    "code": language,
                    "display": language,
                }]
            }
            return self._push("communication", {"language": cc, "preferred": preferred})
        return self._push("communication", {"language": language, "preferred": preferred})

    def add_extension(self, url: str, value: Any) -> "RelatedPersonBuilder":
        extension: Dict[str, Any] = {"url": url}
        if isinstance(value, bool):
            extension["valueBoolean"] = value
        elif isinstance(value, str):
            extension["valueString"] = value
        elif isinstance(value, int):
            extension["valueInteger"] = value
        elif isinstance(value, dict):
            extension.update(value)
        return self._push("extension", extension)

    # ── Backward-compatible convenience aliases (previous API) ──
    def identifier(self, system: str, value: str) -> "RelatedPersonBuilder":
        return self.add_identifier(system, value)

    def patient(self, reference: str, display: Optional[str] = None) -> "RelatedPersonBuilder":
        return self.set_patient(reference, display)

    def relationship(self, codeable_concept: dict) -> "RelatedPersonBuilder":
        return self.add_relationship(codeable_concept)

    def name(self, use: Optional[str] = None, family: Optional[str] = None, given: Optional[List[str]] = None, text: Optional[str] = None) -> "RelatedPersonBuilder":
        nm: dict = {}
        if use:
            nm["use"] = use
        if family:
            nm["family"] = family
        if given:
            nm["given"] = given
        if text:
            nm["text"] = text
        return self._push("name", nm) if nm else self

    def telecom(self, system: str, value: str, use: Optional[str] = None) -> "RelatedPersonBuilder":
        return self.add_telecom(system, value, use or "home")

    def gender(self, value: str) -> "RelatedPersonBuilder":
        return self.set_gender(value)

    def birth_date(self, value: str) -> "RelatedPersonBuilder":
        return self.set_birth_date(value)

    def address(self, use: Optional[str] = None, line: Optional[List[str]] = None, city: Optional[str] = None, district: Optional[str] = None, state: Optional[str] = None, postal_code: Optional[str] = None, country: Optional[str] = None) -> "RelatedPersonBuilder":
        addr: dict = {}
        if use:
            addr["use"] = use
        if line:
            addr["line"] = line
        if city:
            addr["city"] = city
        if district:
            addr["district"] = district
        if state:
            addr["state"] = state
        if postal_code:
            addr["postalCode"] = postal_code
        if country:
            addr["country"] = country
        return self._push("address", addr) if addr else self

    def active(self, value: bool) -> "RelatedPersonBuilder":
        return self.set_active(value)
