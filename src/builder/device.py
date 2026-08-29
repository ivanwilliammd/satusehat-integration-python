from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class DeviceBuilder(BaseBuilder):
    _resourceType = "Device"

    def __init__(self) -> None:
        super().__init__("Device")

    def udi_carrier(self, carrier_aidc: Optional[str] = None, carrier_hrf: Optional[str] = None, device_identifier: Optional[str] = None, issuer: Optional[str] = None, jurisdiction: Optional[str] = None, entry_type: Optional[str] = None) -> "DeviceBuilder":
        u: dict = {}
        if carrier_aidc:
            u["carrierAIDC"] = carrier_aidc
        if carrier_hrf:
            u["carrierHRF"] = carrier_hrf
        if device_identifier:
            u["deviceIdentifier"] = device_identifier
        if issuer:
            u["issuer"] = issuer
        if jurisdiction:
            u["jurisdiction"] = jurisdiction
        if entry_type:
            u["entryType"] = entry_type
        return self._set("udiCarrier", u) if u else self

    def status(self, value: str) -> "DeviceBuilder":
        return self._set("status", value)

    def status_reason(self, codeable_concept: dict) -> "DeviceBuilder":
        return self._append("statusReason", codeable_concept)

    def distinct_identifier(self, value: str) -> "DeviceBuilder":
        return self._set("distinctIdentifier", value)

    def manufacturer(self, value: str) -> "DeviceBuilder":
        return self._set("manufacturerString", value)

    def manufacture_date(self, value: str) -> "DeviceBuilder":
        return self._set("manufactureDate", value)

    def expiration_date(self, value: str) -> "DeviceBuilder":
        return self._set("expirationDate", value)

    def lot_number(self, value: str) -> "DeviceBuilder":
        return self._set("lotNumber", value)

    def serial_number(self, value: str) -> "DeviceBuilder":
        return self._set("serialNumber", value)

    def device_name(self, name: str, type_: str = "user-defined-name") -> "DeviceBuilder":
        return self._append("deviceName", {"name": name, "type": type_})

    def model_number(self, value: str) -> "DeviceBuilder":
        return self._set("modelNumber", value)

    def part_number(self, value: str) -> "DeviceBuilder":
        return self._set("partNumber", value)

    def type(self, codeable_concept: dict) -> "DeviceBuilder":
        return self._set("type", codeable_concept)

    def specialty(self, codeable_concept: dict) -> "DeviceBuilder":
        return self._set("specialty", codeable_concept)

    def version(self, type_codeable_concept: Optional[dict] = None, value: Optional[str] = None) -> "DeviceBuilder":
        v: dict = {}
        if type_codeable_concept:
            v["type"] = type_codeable_concept
        if value:
            v["value"] = value
        return self._append("version", v) if v else self

    def property(self, type_codeable_concept: dict, value: dict) -> "DeviceBuilder":
        return self._append("property", {"type": type_codeable_concept, "value": value})

    def patient(self, reference: str, display: Optional[str] = None) -> "DeviceBuilder":
        pt: dict = {"reference": reference}
        if display:
            pt["display"] = display
        return self._set("patient", pt)

    def owner(self, reference: str, display: Optional[str] = None) -> "DeviceBuilder":
        own: dict = {"reference": reference}
        if display:
            own["display"] = display
        return self._set("owner", own)

    def location(self, reference: str, display: Optional[str] = None) -> "DeviceBuilder":
        loc: dict = {"reference": reference}
        if display:
            loc["display"] = display
        return self._set("location", loc)

    def contact(self, system: str, value: str, use: Optional[str] = None) -> "DeviceBuilder":
        tc: dict = {"system": system, "value": value}
        if use:
            tc["use"] = use
        return self._append("contact", tc)

    def url(self, value: str) -> "DeviceBuilder":
        return self._set("url", value)

    def note(self, text: str) -> "DeviceBuilder":
        return self._append("note", {"text": text})

    def safety(self, codeable_concept: dict) -> "DeviceBuilder":
        return self._append("safety", codeable_concept)

    def identifier(self, system: str, value: str) -> "DeviceBuilder":
        return self._append("identifier", {"system": system, "value": value})
