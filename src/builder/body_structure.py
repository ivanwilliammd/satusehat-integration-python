from typing import List, Optional
from .base import BaseBuilder


class BodyStructureBuilder(BaseBuilder):
    _resourceType = "BodyStructure"

    def __init__(self) -> None:
        super().__init__()

    def identifier(self, system: str, value: str) -> "BodyStructureBuilder":
        return self._append("identifier", {"system": system, "value": value})

    def active(self, value: bool) -> "BodyStructureBuilder":
        return self._set("active", value)

    def morphology(self, codeable_concept: dict) -> "BodyStructureBuilder":
        return self._set("morphology", codeable_concept)

    def location(self, codeable_concept: dict) -> "BodyStructureBuilder":
        return self._set("location", codeable_concept)

    def location_qualifier(self, codeable_concept: dict) -> "BodyStructureBuilder":
        return self._append("locationQualifier", codeable_concept)

    def description(self, value: str) -> "BodyStructureBuilder":
        return self._set("description", value)

    def image(self, content_type: str, url: str) -> "BodyStructureBuilder":
        return self._append("image", {"contentType": content_type, "url": url})

    def patient(self, reference: str, display: Optional[str] = None) -> "BodyStructureBuilder":
        pt: dict = {"reference": reference}
        if display:
            pt["display"] = display
        return self._set("patient", pt)
