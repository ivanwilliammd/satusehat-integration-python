"""HL7 v2 message: an ordered list of segments addressed by name."""

from __future__ import annotations

import re

from .encoding import charset_of
from .segment import Segment


class HL7Error(ValueError):
    """Raised when a message cannot be parsed or fails a hard validation rule."""


class Message:
    def __init__(self, segments: list[Segment], separator: str = "|") -> None:
        self._segments = segments
        self.separator = separator

    @classmethod
    def parse(cls, er7: str) -> "Message":
        cleaned = re.sub(r"[\x0b\x1c]", "", er7).strip()
        if cleaned == "":
            raise HL7Error("Empty HL7 message.")

        segments: list[Segment] = []
        separator = "|"
        for line in re.split(r"\r\n|\r|\n", cleaned):
            if line.strip() == "":
                continue
            sep = line[3] if len(line) > 3 else "|"
            parts = line.split(sep)
            if not parts[0]:
                continue
            if parts[0] == "MSH":
                separator = sep
            segments.append(Segment.from_parts(parts, sep))

        if not segments or segments[0].name != "MSH":
            raise HL7Error("HL7 message must start with an MSH segment.")
        return cls(segments, separator)

    @classmethod
    def from_segments(cls, segments: list[Segment], separator: str = "|") -> "Message":
        return cls(segments, separator)

    def all(self) -> list[Segment]:
        return list(self._segments)

    def segment(self, name: str, occurrence: int = 1) -> Segment | None:
        seen = 0
        for seg in self._segments:
            if seg.name == name:
                seen += 1
                if seen == occurrence:
                    return seg
        return None

    def all_of(self, name: str) -> list[Segment]:
        return [s for s in self._segments if s.name == name]

    def get(self, path: str) -> str:
        name, _, rest = path.partition(".")
        seg = self.segment(name)
        return seg.get(rest) if seg and rest else ""

    def set(self, path: str, value: str) -> "Message":
        name, _, rest = path.partition(".")
        seg = self.segment(name)
        if seg and rest:
            seg.set(rest, value)
        return self

    def message_type(self) -> str:
        return self.get("MSH.9.1")

    def trigger_event(self) -> str:
        return self.get("MSH.9.2")

    def control_id(self) -> str:
        return self.get("MSH.10")

    def version(self) -> str:
        return self.get("MSH.12.1")

    def charset(self) -> str:
        seg = self.segment("MSH")
        return charset_of(seg.field(18) if seg else "")

    def __str__(self) -> str:
        body = "\r".join(str(s) for s in self._segments)
        return "" if body == "" else body + "\r"
