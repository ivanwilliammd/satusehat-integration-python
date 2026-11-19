"""One HL7 v2 segment: fields kept as raw text and split on demand."""

from __future__ import annotations

from .encoding import decode, encode


class Segment:
    """Fields are 1-based because HL7 numbers them from 1; index 0 is never used."""

    def __init__(self, name: str, fields: dict[int, str] | None = None, separator: str = "|") -> None:
        self.name = name
        self.fields: dict[int, str] = dict(fields or {})
        self.separator = separator

    @classmethod
    def from_parts(cls, parts: list[str], separator: str = "|") -> "Segment":
        name = parts[0] if parts else ""
        # MSH is special: MSH-1 is the separator itself and MSH-2 holds the encoding characters,
        # so its split starts one position later than every other segment.
        offset = 1 if name == "MSH" else 0
        fields = {i + 1 + offset: value for i, value in enumerate(parts[1:])}
        if name == "MSH":
            fields[1] = separator
        return cls(name, fields, separator)

    def field(self, n: int) -> str:
        return self.fields.get(n, "")

    def get(self, path: str) -> str:
        """Reads ``5``, ``5.1`` (component) or ``5.1.2`` (subcomponent); first repetition only."""
        parts = path.split(".")
        first = int(parts.pop(0))
        raw = self.field(first)
        value = raw.split("~")[0]
        if not parts:
            return decode(value)
        components = value.split("^")
        idx = int(parts[0]) - 1
        value = components[idx] if idx < len(components) else ""
        if len(parts) > 1:
            subs = value.split("&")
            idx = int(parts[1]) - 1
            value = subs[idx] if idx < len(subs) else ""
        return decode(value)

    def field_all(self, n: int) -> list[str]:
        raw = self.field(n)
        return [] if raw == "" else [decode(r) for r in raw.split("~")]

    def set(self, path: str, value: str) -> "Segment":
        parts = path.split(".")
        n = int(parts.pop(0))
        if not parts:
            self.fields[n] = encode(value)
            return self
        reps = self.field(n).split("~") if self.field(n) != "" else [""]
        components = reps[0].split("^")
        idx = int(parts[0]) - 1
        while len(components) <= idx:
            components.append("")
        components[idx] = encode(value)
        reps[0] = "^".join(components)
        self.fields[n] = "~".join(reps)
        return self

    def __str__(self) -> str:
        highest = max(self.fields) if self.fields else 0
        # MSH keeps its separator in field 1; rendering from field 2 avoids "MSH|||".
        start = 2 if self.name == "MSH" else 1
        out = [self.name] + [self.fields.get(i, "") for i in range(start, highest + 1)]
        while len(out) > 2 and out[-1] == "":
            out.pop()
        return self.separator.join(out)
