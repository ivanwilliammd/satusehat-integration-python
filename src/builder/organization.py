from typing import Any, Dict, Optional

from src.datatype.datatypes import Identifier, Address, ContactPoint
from src.builder.base_builder import BaseBuilder


class OrganizationBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Organization")

    def add_identifier(self, identifier: Identifier) -> "OrganizationBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append(identifier.to_array() if hasattr(identifier, "to_array") else identifier)
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
        self.data["telecom"].append(telecom.to_array() if hasattr(telecom, "to_array") else telecom)
        return self

    def add_address(self, address: Address) -> "OrganizationBuilder":
        if "address" not in self.data:
            self.data["address"] = []
        self.data["address"].append(address.to_array() if hasattr(address, "to_array") else address)
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
        type_code: Any,
        type_display: Optional[str] = None,
    ) -> "OrganizationBuilder":
        # FHIR R4: organization.type adalah 0..*, jadi setiap panggilan menambah — bukan menimpa.
        if isinstance(type_code, str):
            entry: Dict[str, Any] = {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                    "code": type_code,
                    "display": type_display,
                }]
            }
        else:
            entry = type_code.to_array() if hasattr(type_code, "to_array") else type_code
        self.data.setdefault("type", []).append(entry)
        return self

    def set_id(self, id: str) -> "OrganizationBuilder":
        self.data["id"] = id
        return self

    def set_active(self, active: bool) -> "OrganizationBuilder":
        self.data["active"] = active
        return self

    def add_contact(self, telecom: Any, purpose: Optional[str] = None, name: Optional[str] = None,
                    address: Any = None) -> "OrganizationBuilder":
        arr = lambda v: v.to_array() if hasattr(v, "to_array") else v
        contact: Dict[str, Any] = {"telecom": [arr(telecom)]}
        if purpose is not None:
            contact["purpose"] = {"text": purpose}
        if name is not None:
            contact["name"] = {"text": name}
        if address is not None:
            contact["address"] = arr(address)
        self.data.setdefault("contact", []).append(contact)
        return self

    def add_endpoint(self, endpoint: Any) -> "OrganizationBuilder":
        entry = {"reference": endpoint} if isinstance(endpoint, str) else (
            endpoint.to_array() if hasattr(endpoint, "to_array") else endpoint
        )
        self.data.setdefault("endpoint", []).append(entry)
        return self

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "OrganizationBuilder":
        extension: Dict[str, Any] = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        self.data.setdefault("extension", []).append(extension)
        return self
