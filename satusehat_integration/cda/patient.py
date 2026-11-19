"""The patient identity block: identifiers, name, sex and birth date.

Identifiers keep their full (root, extension) pair. A NIK without its root cannot be matched against
anything, and dropping the root is how a local MRN silently becomes a national NIK.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PatientRole:
    identifiers: list[dict[str, str]] = field(default_factory=list)
    names: list[str] = field(default_factory=list)
    administrative_gender: str = ""
    birth_time: str = ""

    def name(self) -> str:
        return self.names[0] if self.names else ""

    def identifier(self, root: str) -> str:
        for item in self.identifiers:
            if item.get("root") == root:
                return item.get("extension", "")
        return ""
