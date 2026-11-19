"""One CDA section: a coded heading with narrative text and, optionally, nested sections.

Narrative is kept as XML rather than as plain text because CDA narrative carries ``<content>``,
``<paragraph>`` and referenced elements; flattening at parse time would destroy the only
human-readable part of the document.
"""

from __future__ import annotations

from dataclasses import dataclass, field

LOINC = "2.16.840.1.113883.6.1"


@dataclass
class Section:
    title: str = ""
    text: str = ""
    codes: dict[str, str] = field(default_factory=dict)
    children: list["Section"] = field(default_factory=list)

    def code(self) -> str | None:
        """LOINC code of this section, e.g. "10164-2" for History of present illness."""
        if LOINC in self.codes:
            return self.codes[LOINC]
        return next(iter(self.codes.values()), None)

    def find(self, loinc: str) -> "Section | None":
        """First section in the tree with this LOINC code, depth first."""
        if self.codes.get(LOINC) == loinc:
            return self
        for child in self.children:
            hit = child.find(loinc)
            if hit is not None:
                return hit
        return None

    def flatten(self) -> list["Section"]:
        out = [self]
        for child in self.children:
            out.extend(child.flatten())
        return out
