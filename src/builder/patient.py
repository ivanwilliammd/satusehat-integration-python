from src.datatype.datatypes import Identifier, HumanName, Address, ContactPoint
from src.builder.base_builder import BaseBuilder


class PatientBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Patient")

    def add_identifier(self, identifier: Identifier) -> "PatientBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append(identifier.to_array())
        return self

    def add_name(self, name: HumanName) -> "PatientBuilder":
        if "name" not in self.data:
            self.data["name"] = []
        self.data["name"].append(name.to_array())
        return self

    def add_telecom(self, telecom: ContactPoint) -> "PatientBuilder":
        if "telecom" not in self.data:
            self.data["telecom"] = []
        self.data["telecom"].append(telecom.to_array())
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
        self.data["address"].append(address.to_array())
        return self

    def set_marital_status(self, text: str) -> "PatientBuilder":
        self.data["maritalStatus"] = {"text": text}
        return self

    def add_communication(self, language: str, preferred: bool = False) -> "PatientBuilder":
        if "communication" not in self.data:
            self.data["communication"] = []
        self.data["communication"].append({
            "language": {"text": language},
            "preferred": preferred,
        })
        return self
