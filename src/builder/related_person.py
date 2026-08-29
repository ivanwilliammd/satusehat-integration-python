from typing import List, Optional
from .base import BaseBuilder


class RelatedPersonBuilder(BaseBuilder):
    _resourceType = "RelatedPerson"

    def __init__(self) -> None:
        super().__init__()

    def active(self, value: bool) -> "RelatedPersonBuilder":
        return self._set("active", value)

    def patient(self, reference: str, display: Optional[str] = None) -> "RelatedPersonBuilder":
        pt: dict = {"reference": reference}
        if display:
            pt["display"] = display
        return self._set("patient", pt)

    def relationship(self, codeable_concept: dict) -> "RelatedPersonBuilder":
        return self._append("relationship", codeable_concept)

    def name(self, use: Optional[str] = None, family: Optional[str] = None, given: Optional[List[str]] = None, text: Optional[str] = None) -> "RelatedPersonBuilder":
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

    def telecom(self, system: str, value: str, use: Optional[str] = None) -> "RelatedPersonBuilder":
        tc: dict = {"system": system, "value": value}
        if use:
            tc["use"] = use
        return self._append("telecom", tc)

    def gender(self, value: str) -> "RelatedPersonBuilder":
        return self._set("gender", value)

    def birth_date(self, value: str) -> "RelatedPersonBuilder":
        return self._set("birthDate", value)

    def address(self, use: Optional[str] = None, line: Optional[List[str]] = None, city: Optional[str] = None, district: Optional[str] = None, state: Optional[str] = None, postal_code: Optional[str] = None, country: Optional[str] = None) -> "RelatedPersonBuilder":
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

    def photo(self, content_type: str, url: str) -> "RelatedPersonBuilder":
        return self._append("photo", {"contentType": content_type, "url": url})

    def period(self, start: Optional[str] = None, end: Optional[str] = None) -> "RelatedPersonBuilder":
        p: dict = {}
        if start:
            p["start"] = start
        if end:
            p["end"] = end
        return self._set("period", p) if p else self

    def identifier(self, system: str, value: str) -> "RelatedPersonBuilder":
        return self._append("identifier", {"system": system, "value": value})
