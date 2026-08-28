from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Identifier:
    system: str
    value: str

@dataclass
class Coding:
    system: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None

@dataclass
class CodeableConcept:
    coding: List[Coding] = field(default_factory=list)
    text: Optional[str] = None

@dataclass
class Reference:
    reference: Optional[str] = None
    display: Optional[str] = None
