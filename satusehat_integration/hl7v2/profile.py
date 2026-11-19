"""Declarative validation profiles.

Profiles are data, not a class per message type: every LIS and every hospital disagrees about the
details, so a new vendor is a new dict, not a file ported to five languages.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .message import HL7Error, Message


@dataclass
class Issue:
    severity: str  # "error" | "warning"
    path: str
    message: str


@dataclass
class Profile:
    name: str
    message_type: str | None = None
    trigger: str | None = None
    required_segments: list[str] = field(default_factory=list)
    required_fields: dict[str, str] = field(default_factory=dict)
    allowed_values: dict[str, list[str]] = field(default_factory=dict)

    def validate(self, message: Message) -> list[Issue]:
        issues: list[Issue] = []
        if self.message_type and message.message_type() != self.message_type:
            issues.append(
                Issue("error", "MSH.9.1", f"message type {message.message_type()} is not {self.message_type}")
            )
        if self.trigger and message.trigger_event() != self.trigger:
            issues.append(Issue("error", "MSH.9.2", f"trigger {message.trigger_event()} is not {self.trigger}"))
        for name in self.required_segments:
            if message.segment(name) is None:
                issues.append(Issue("error", name, "required segment missing"))
        for path, label in self.required_fields.items():
            if message.get(path).strip() == "":
                issues.append(Issue("error", path, f"required ({label})"))
        for path, allowed in self.allowed_values.items():
            value = message.get(path)
            if value and value not in allowed:
                issues.append(
                    Issue("warning", path, f"'{value}' is outside the usual set ({', '.join(allowed)})")
                )
        return issues

    def passes(self, message: Message) -> bool:
        return all(i.severity != "error" for i in self.validate(message))

    def assert_passes(self, message: Message) -> None:
        errors = [i for i in self.validate(message) if i.severity == "error"]
        if errors:
            raise HL7Error("; ".join(f"{e.path}: {e.message}" for e in errors))
