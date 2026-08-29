from typing import List, Optional
from .base import BaseBuilder


class FlagBuilder(BaseBuilder):
    _resourceType = "Flag"

    def __init__(self) -> None:
        super().__init__()

    def status(self, value: str) -> "FlagBuilder":
        return self._set("status", value)

    def category(self, codeable_concept: dict) -> "FlagBuilder":
        return self._set("category", codeable_concept)

    def code(self, codeable_concept: dict) -> "FlagBuilder":
        return self._set("code", codeable_concept)

    def subject(self, reference: str, display: Optional[str] = None) -> "FlagBuilder":
        sub: dict = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("subject", sub)

    def encounter(self, reference: str) -> "FlagBuilder":
        return self._set("encounter", {"reference": reference})

    def period(self, start: Optional[str] = None, end: Optional[str] = None) -> "FlagBuilder":
        p: dict = {}
        if start:
            p["start"] = start
        if end:
            p["end"] = end
        return self._set("period", p) if p else self

    def author(self, reference: str, display: Optional[str] = None) -> "FlagBuilder":
        auth: dict = {"reference": reference}
        if display:
            auth["display"] = display
        return self._set("author", auth)
