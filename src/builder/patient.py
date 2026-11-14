from typing import Any, Optional

from src.datatype.datatypes import Identifier, HumanName, Address, ContactPoint
from src.builder.base_builder import BaseBuilder


def _arr(value: Any) -> Any:
    return value.to_array() if hasattr(value, "to_array") else value


class PatientBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Patient")

    def add_identifier(self, identifier: Identifier) -> "PatientBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append(_arr(identifier))
        return self

    def add_name(self, name: HumanName) -> "PatientBuilder":
        if "name" not in self.data:
            self.data["name"] = []
        self.data["name"].append(_arr(name))
        return self

    def add_telecom(self, telecom: ContactPoint) -> "PatientBuilder":
        if "telecom" not in self.data:
            self.data["telecom"] = []
        self.data["telecom"].append(_arr(telecom))
        return self

    def set_gender(self, gender: str) -> "PatientBuilder":
        self.data["gender"] = gender
        return self

    def set_birth_date(self, birth_date: str) -> "PatientBuilder":
        self.data["birthDate"] = birth_date
        return self

    def add_address(self, address: Address) -> "PatientBuilder":
        if "address" not in self.data:
            self.data["address"] = []
        self.data["address"].append(_arr(address))
        return self

    def set_meta_profile(self, profile: str) -> "PatientBuilder":
        self.data.setdefault("meta", {})["profile"] = [profile]
        return self

    def set_id(self, id: str) -> "PatientBuilder":
        self.data["id"] = id
        return self

    def set_active(self, active: bool) -> "PatientBuilder":
        self.data["active"] = active
        return self

    def set_marital_status(self, marital_status: Any, display: Optional[str] = None,
                           system: str = "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus") -> "PatientBuilder":
        # FHIR R4: maritalStatus adalah CodeableConcept. Teks saja tetap diterima untuk API lama.
        if isinstance(marital_status, str):
            if display is None and len(marital_status) > 2:
                self.data["maritalStatus"] = {"text": marital_status}
            else:
                self.data["maritalStatus"] = {
                    "coding": [{"system": system, "code": marital_status, "display": display or marital_status}]
                }
        else:
            self.data["maritalStatus"] = _arr(marital_status)
        return self

    def add_communication(self, language: Any, preferred: bool = True) -> "PatientBuilder":
        if isinstance(language, str):
            kode = {"coding": [{"system": "urn:ietf:bcp:47", "code": language}]}
        else:
            kode = _arr(language)
        return self._push("communication", {"language": kode, "preferred": preferred})

    def set_deceased_boolean(self, deceased: bool) -> "PatientBuilder":
        self.data["deceasedBoolean"] = deceased
        return self

    def set_deceased_date_time(self, date_time: str) -> "PatientBuilder":
        self.data["deceasedDateTime"] = date_time
        return self

    def set_multiple_birth_boolean(self, multiple_birth: bool) -> "PatientBuilder":
        self.data["multipleBirthBoolean"] = multiple_birth
        return self

    def set_multiple_birth_integer(self, multiple_birth: int) -> "PatientBuilder":
        self.data["multipleBirthInteger"] = multiple_birth
        return self

    def add_contact(self, relationship: Any = None, name: Any = None, telecom: Any = None,
                    address: Any = None, gender: Optional[str] = None,
                    organization: Any = None) -> "PatientBuilder":
        contact: dict = {}
        if relationship is not None:
            contact["relationship"] = [_arr(relationship)]
        if name is not None:
            contact["name"] = _arr(name)
        if telecom is not None:
            contact["telecom"] = [_arr(telecom)]
        if address is not None:
            contact["address"] = _arr(address)
        if gender is not None:
            contact["gender"] = gender
        if organization is not None:
            contact["organization"] = _arr(organization)
        return self._push("contact", contact)

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "PatientBuilder":
        extension: dict = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        return self._push("extension", extension)
