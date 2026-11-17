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

    def get_udi_carrier(self) -> Any:
        return self._data.get("udiCarrier")

    getUdiCarrier = get_udi_carrier

    def get_status_reason(self) -> Any:
        return self._data.get("statusReason")

    getStatusReason = get_status_reason

    def get_distinct_identifier(self) -> Any:
        return self._data.get("distinctIdentifier")

    getDistinctIdentifier = get_distinct_identifier

    def get_manufacture_date(self) -> Any:
        return self._data.get("manufactureDate")

    getManufactureDate = get_manufacture_date

    def get_expiration_date(self) -> Any:
        return self._data.get("expirationDate")

    getExpirationDate = get_expiration_date

    def get_lot_number(self) -> Any:
        return self._data.get("lotNumber")

    getLotNumber = get_lot_number

    def get_serial_number(self) -> Any:
        return self._data.get("serialNumber")

    getSerialNumber = get_serial_number

    def get_model_number(self) -> Any:
        return self._data.get("modelNumber")

    getModelNumber = get_model_number

    def get_part_number(self) -> Any:
        return self._data.get("partNumber")

    getPartNumber = get_part_number

    def get_specialty(self) -> Any:
        return self._data.get("specialty")

    getSpecialty = get_specialty

    def get_patient(self) -> Any:
        return self._data.get("patient")

    getPatient = get_patient

    def get_owner(self) -> Any:
        return self._data.get("owner")

    getOwner = get_owner

    def get_location(self) -> Any:
        return self._data.get("location")

    getLocation = get_location

    def get_url(self) -> Any:
        return self._data.get("url")

    getUrl = get_url

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_device_name(self) -> Any:
        return self._data.get("deviceName")

    getDeviceName = get_device_name

    def get_version(self) -> Any:
        return self._data.get("version")

    getVersion = get_version

    def get_property(self) -> Any:
        return self._data.get("property")

    getProperty = get_property

    def get_contact(self) -> Any:
        return self._data.get("contact")

    getContact = get_contact

    def get_note(self) -> Any:
        return self._data.get("note")

    getNote = get_note

    def get_safety(self) -> Any:
        return self._data.get("safety")

    getSafety = get_safety

    def get_identifier(self) -> Any:
        return self._data.get("identifier")

    getIdentifier = get_identifier
