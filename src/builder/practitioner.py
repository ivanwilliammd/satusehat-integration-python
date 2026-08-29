from src.datatype.datatypes import Identifier, HumanName, Address, ContactPoint
from src.builder.base_builder import BaseBuilder


class PractitionerBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Practitioner")

    def add_identifier(self, identifier: Identifier) -> "PractitionerBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append(identifier.to_array())
        return self

    def add_name(self, name: HumanName) -> "PractitionerBuilder":
        if "name" not in self.data:
            self.data["name"] = []
        self.data["name"].append(name.to_array())
        return self

    def add_telecom(self, telecom: ContactPoint) -> "PractitionerBuilder":
        if "telecom" not in self.data:
            self.data["telecom"] = []
        self.data["telecom"].append(telecom.to_array())
        return self

    def add_address(self, address: Address) -> "PractitionerBuilder":
        if "address" not in self.data:
            self.data["address"] = []
        self.data["address"].append(address.to_array())
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
