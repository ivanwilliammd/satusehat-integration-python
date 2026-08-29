from typing import Any, Dict, Optional

from src.datatype.datatypes import Identifier, Address, ContactPoint
from src.builder.base_builder import BaseBuilder


class OrganizationBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Organization")

    def add_identifier(self, identifier: Identifier) -> "OrganizationBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append(identifier.to_array())
        return self

    def set_name(self, name: str) -> "OrganizationBuilder":
        self.data["name"] = name
        return self

    def add_alias(self, alias: str) -> "OrganizationBuilder":
        if "alias" not in self.data:
            self.data["alias"] = []
        self.data["alias"].append(alias)
        return self

    def add_telecom(self, telecom: ContactPoint) -> "OrganizationBuilder":
        if "telecom" not in self.data:
            self.data["telecom"] = []
        self.data["telecom"].append(telecom.to_array())
        return self

    def add_address(self, address: Address) -> "OrganizationBuilder":
        if "address" not in self.data:
            self.data["address"] = []
        self.data["address"].append(address.to_array())
        return self

    def set_part_of(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "OrganizationBuilder":
        part: Dict[str, Any] = {"reference": reference}
        if display:
            part["display"] = display
        self.data["partOf"] = part
        return self

    def set_type(
        self,
        type_code: str,
        type_display: Optional[str] = None,
    ) -> "OrganizationBuilder":
        self.data["type"] = {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                "code": type_code,
                "display": type_display,
            }]
        }
        return self
