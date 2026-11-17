from typing import Any, Optional
from satusehat_integration.datatype.datatypes import Identifier, HumanName, Address, ContactPoint
from satusehat_integration.builder.base_builder import BaseBuilder


class PractitionerBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Practitioner")

    def add_identifier(self, identifier: Identifier) -> "PractitionerBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append(identifier.to_array() if hasattr(identifier, "to_array") else identifier)
        return self

    def add_name(self, name: HumanName) -> "PractitionerBuilder":
        if "name" not in self.data:
            self.data["name"] = []
        self.data["name"].append(name.to_array() if hasattr(name, "to_array") else name)
        return self

    def add_telecom(self, telecom: ContactPoint) -> "PractitionerBuilder":
        if "telecom" not in self.data:
            self.data["telecom"] = []
        self.data["telecom"].append(telecom.to_array() if hasattr(telecom, "to_array") else telecom)
        return self

    def add_address(self, address: Address) -> "PractitionerBuilder":
        if "address" not in self.data:
            self.data["address"] = []
        self.data["address"].append(address.to_array() if hasattr(address, "to_array") else address)
        return self

    def set_gender(self, gender: str) -> "PractitionerBuilder":
        self.data["gender"] = gender
        return self

    def set_birth_date(self, birth_date: str) -> "PractitionerBuilder":
        self.data["birthDate"] = birth_date
        return self

    def add_qualification(
        self,
        code: str,
        display: str,
        system: str = "http://terminology.hl7.org/CodeSystem/v2-0360",
    ) -> "PractitionerBuilder":
        if "qualification" not in self.data:
            self.data["qualification"] = []
        self.data["qualification"].append({
            "code": {
                "coding": [{"system": system, "code": code, "display": display}]
            }
        })
        return self

    # --- Nama kanon (cermin PayloadBuilderPractitioner) ---

    def set_id(self, id: str) -> "PractitionerBuilder":
        self.data["id"] = id
        return self

    def set_active(self, active: bool) -> "PractitionerBuilder":
        self.data["active"] = active
        return self

    def add_photo(self, url: str, content_type: Optional[str] = None) -> "PractitionerBuilder":
        photo: Dict[str, Any] = {"url": url}
        if content_type is not None:
            photo["contentType"] = content_type
        self.data.setdefault("photo", []).append(photo)
        return self

    def add_qualification_canonical(self, identifier: Any, code: Any,
                                    period_start: Optional[str] = None,
                                    issuer: Any = None) -> "PractitionerBuilder":
        """Bentuk kanon: identifier + code + period.start + issuer. add_qualification lama tetap ada."""
        arr = lambda v: v.to_array() if hasattr(v, "to_array") else v
        qualification: Dict[str, Any] = {"identifier": [arr(identifier)], "code": arr(code)}
        if period_start is not None:
            qualification["period"] = {"start": period_start}
        if issuer is not None:
            qualification["issuer"] = arr(issuer)
        self.data.setdefault("qualification", []).append(qualification)
        return self

    def add_communication(self, language: Any, preferred: Optional[bool] = None) -> "PractitionerBuilder":
        entry: Dict[str, Any] = {
            "language": language.to_array() if hasattr(language, "to_array") else language
        }
        if preferred is not None:
            entry["preferred"] = preferred
        self.data.setdefault("communication", []).append(entry)
        return self

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "PractitionerBuilder":
        extension: Dict[str, Any] = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        self.data.setdefault("extension", []).append(extension)
        return self
