from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class PersonBuilder(BaseBuilder):
    _resourceType = "Person"

    def __init__(self) -> None:
        super().__init__("PersonBuilder")

    def identifier(self, system: str, value: str) -> "PersonBuilder":
        return self._append("identifier", {"system": system, "value": value})

    def name(self, use: Optional[str] = None, family: Optional[str] = None, given: Optional[List[str]] = None, text: Optional[str] = None) -> "PersonBuilder":
        nm: dict = {}
        if use:
            nm["use"] = use
        if family:
            nm["family"] = family
        if given:
            nm["given"] = given
        if text:
            nm["text"] = text
        return self._append("name", nm) if nm else self

    def telecom(self, system: str, value: str, use: Optional[str] = None) -> "PersonBuilder":
        tc: dict = {"system": system, "value": value}
        if use:
            tc["use"] = use
        return self._append("telecom", tc)

    def gender(self, value: str) -> "PersonBuilder":
        return self._set("gender", value)

    def birth_date(self, value: str) -> "PersonBuilder":
        return self._set("birthDate", value)

    def address(self, use: Optional[str] = None, line: Optional[List[str]] = None, city: Optional[str] = None, district: Optional[str] = None, state: Optional[str] = None, postal_code: Optional[str] = None, country: Optional[str] = None) -> "PersonBuilder":
        addr: dict = {}
        if use:
            addr["use"] = use
        if line:
            addr["line"] = line
        if city:
            addr["city"] = city
        if district:
            addr["district"] = district
        if state:
            addr["state"] = state
        if postal_code:
            addr["postalCode"] = postal_code
        if country:
            addr["country"] = country
        return self._append("address", addr) if addr else self

    def photo(self, content_type: str, url: str) -> "PersonBuilder":
        return self._set("photo", {"contentType": content_type, "url": url})

    def managing_organization(self, reference: str, display: Optional[str] = None) -> "PersonBuilder":
        org: dict = {"reference": reference}
        if display:
            org["display"] = display
        return self._set("managingOrganization", org)

    def active(self, value: bool) -> "PersonBuilder":
        return self._set("active", value)

    def link(self, target: dict, assurance: Optional[str] = None) -> "PersonBuilder":
        lnk: dict = {"target": target}
        if assurance:
            lnk["assurance"] = assurance
        return self._append("link", lnk)
