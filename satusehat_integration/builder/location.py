from typing import Any, Dict, Optional

from satusehat_integration.datatype.datatypes import Identifier, Address, ContactPoint
from satusehat_integration.builder.base_builder import BaseBuilder


class LocationBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("Location")

    def add_identifier(self, identifier: Identifier) -> "LocationBuilder":
        if "identifier" not in self.data:
            self.data["identifier"] = []
        self.data["identifier"].append(identifier.to_array() if hasattr(identifier, "to_array") else identifier)
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
        self.data["telecom"].append(telecom.to_array() if hasattr(telecom, "to_array") else telecom)
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

    # --- Nama kanon (cermin PayloadBuilderLocation) ---

    def set_id(self, id: str) -> "LocationBuilder":
        self.data["id"] = id
        return self

    def set_operational_status(self, status: Any) -> "LocationBuilder":
        self.data["operationalStatus"] = status.to_array() if hasattr(status, "to_array") else status
        return self

    def add_alias(self, alias: str) -> "LocationBuilder":
        self.data.setdefault("alias", []).append(alias)
        return self

    def set_type(self, location_type: Any) -> "LocationBuilder":
        entry = location_type.to_array() if hasattr(location_type, "to_array") else location_type
        self.data.setdefault("type", []).append(entry)
        return self

    def add_address(self, address: Any) -> "LocationBuilder":
        entry = address.to_array() if hasattr(address, "to_array") else address
        self.data.setdefault("address", []).append(entry)
        return self

    def set_position(self, latitude: Optional[float] = None, longitude: Optional[float] = None,
                     altitude: Optional[float] = None) -> "LocationBuilder":
        position: Dict[str, Any] = {}
        if latitude is not None:
            position["latitude"] = latitude
        if longitude is not None:
            position["longitude"] = longitude
        if altitude is not None:
            position["altitude"] = altitude
        self.data["position"] = position
        return self

    def add_endpoint(self, endpoint: Any) -> "LocationBuilder":
        entry = {"reference": endpoint} if isinstance(endpoint, str) else (
            endpoint.to_array() if hasattr(endpoint, "to_array") else endpoint
        )
        self.data.setdefault("endpoint", []).append(entry)
        return self

    def add_extension(self, url: str, value: Any, value_type: Optional[str] = None) -> "LocationBuilder":
        extension: Dict[str, Any] = {"url": url}
        if value_type is not None:
            extension["value" + value_type[:1].upper() + value_type[1:]] = value
        else:
            extension["valueString"] = value
        self.data.setdefault("extension", []).append(extension)
        return self
