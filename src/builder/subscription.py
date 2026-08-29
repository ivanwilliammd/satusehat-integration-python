"""Subscription resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class SubscriptionBuilder(BaseBuilder):
    """Builder for Subscription resource."""

    def __init__(self):
        super().__init__("SubscriptionBuilder")
        self.data = {"resourceType": "Subscription"}

    def set_id(self, id: str) -> "SubscriptionBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str) -> "SubscriptionBuilder":
        self.data["status"] = status
        return self

    def set_contact(self, system: str, value: str) -> "SubscriptionBuilder":
        self.data.setdefault("contact", [])
        self.data["contact"].append({"system": system, "value": value})
        return self

    def set_end(self, end: str) -> "SubscriptionBuilder":
        self.data["end"] = end
        return self

    def set_reason(self, reason: str) -> "SubscriptionBuilder":
        self.data["reason"] = reason
        return self

    def set_criteria(self, criteria: str) -> "SubscriptionBuilder":
        self.data["criteria"] = criteria
        return self

    def set_channel_type(self, code: str, system: str) -> "SubscriptionBuilder":
        self.data["channelType"] = {"coding": [{"code": code, "system": system}]}
        return self

    def set_channel_endpoint(self, endpoint: str) -> "SubscriptionBuilder":
        self.data.setdefault("channel", {})["endpoint"] = endpoint
        return self

    def set_channel_header(self, header: str) -> "SubscriptionBuilder":
        self.data.setdefault("channel", {})["header"] = header
        return self

    def set_channel_payload(self, content_type: str) -> "SubscriptionBuilder":
        self.data.setdefault("channel", {})["payload"] = content_type
        return self

    def add_tag(self, code: str, system: str, display: Optional[str] = None) -> "SubscriptionBuilder":
        self.data.setdefault("tag", [])
        tag: dict = {"coding": [{"system": system, "code": code}]}
        if display:
            tag["coding"][0]["display"] = display
        self.data["tag"].append(tag)
        return self
