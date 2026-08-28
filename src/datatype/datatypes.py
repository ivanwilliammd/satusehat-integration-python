from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Identifier:
    system: str
    value: str
    def to_array(self): return {"system": self.system, "value": self.value}

@dataclass
class HumanName:
    use: Optional[str] = None
    text: Optional[str] = None
    family: Optional[str] = None
    given: List[str] = field(default_factory=list)
    def to_array(self):
        res = {}
        if self.use: res["use"] = self.use
        if self.text: res["text"] = self.text
        if self.family: res["family"] = self.family
        if self.given: res["given"] = self.given
        return res

@dataclass
class Address:
    line: List[str] = field(default_factory=list)
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    def to_array(self):
        res = {}
        if self.line: res["line"] = self.line
        if self.city: res["city"] = self.city
        if self.district: res["district"] = self.district
        if self.state: res["state"] = self.state
        if self.postalCode: res["postalCode"] = self.postalCode
        if self.country: res["country"] = self.country
        return res

@dataclass
class ContactPoint:
    system: Optional[str] = None
    value: Optional[str] = None
    use: Optional[str] = None
    def to_array(self):
        return {"system": self.system, "value": self.value, "use": self.use}

@dataclass
class Coding:
    system: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None
    def to_array(self):
        return {"system": self.system, "code": self.code, "display": self.display}

@dataclass
class CodeableConcept:
    coding: List[Coding] = field(default_factory=list)
    text: Optional[str] = None
    def to_array(self):
        return {"coding": [c.to_array() for c in self.coding], "text": self.text}

@dataclass
class Reference:
    reference: Optional[str] = None
    display: Optional[str] = None
    def to_array(self):
        return {"reference": self.reference, "display": self.display}
