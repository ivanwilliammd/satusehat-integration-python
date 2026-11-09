"""DeviceParser — parses FHIR Device resource."""
from __future__ import annotations

from typing import Any, Optional


class DeviceParser:
    def __init__(self, device: Optional[dict[str, Any]] = None) -> None:
        self.device: dict[str, Any] = device if isinstance(device, dict) else {}

    def get_identifiers(self) -> Any:
        return self.device.get("identifier")

    getIdentifiers = get_identifiers

    def get_status(self) -> Any:
        return self.device.get("status")

    getStatus = get_status

    def get_manufacturer(self) -> Any:
        return self.device.get("manufacturer")

    getManufacturer = get_manufacturer

    def get_device_names(self) -> Any:
        return self.device.get("deviceName")

    getDeviceNames = get_device_names

    def get_type(self) -> Any:
        return self.device.get("type")

    getType = get_type
