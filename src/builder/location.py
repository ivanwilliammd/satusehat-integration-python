from typing import Any, Dict, Optional

from src.datatype.datatypes import Identifier, Address, ContactPoint
from src.builder.base_builder import BaseBuilder


class LocationBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Location")

    def add_identifier(self, identifier: Identifier) -> "LocationBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append(identifier.to_array())
        return self

    def set_status(self, status: str) -> "LocationBuilder":
        self.data["status"] = status
        return self

    def set_name(self, name: str) -> "LocationBuilder":
        self.data["name"] = name
        return self

    def set_description(self, description: str) -> "LocationBuilder":
        self.data["description"] = description
        return self

    def add_telecom(self, telecom: ContactPoint) -> "LocationBuilder":
        if "telecom" not in self.data:
            self.data["telecom"] = []
        self.data["telecom"].append(telecom.to_array())
        return self

    def set_address(self, address: Address) -> "LocationBuilder":
        self.data["address"] = address.to_array()
        return self

    def set_part_of(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "LocationBuilder":
        part: Dict[str, Any] = {"reference": reference}
        if display:
            part["display"] = display
        self.data["partOf"] = part
        return self

    def set_physical_type(
        self,
        code: str,
        display: Optional[str] = None,
    ) -> "LocationBuilder":
        self.data["physicalType"] = {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/location-physical-type",
                "code": code,
                "display": display,
            }]
        }
        return self

    def set_managing_organization(
        self,
        reference: str,
        display: Optional[str] = None,
    ) -> "LocationBuilder":
        org: Dict[str, Any] = {"reference": reference}
        if display:
            org["display"] = display
        self.data["managingOrganization"] = org
        return self
