"""GroupParser — parses FHIR Group resource."""
from __future__ import annotations

from typing import Any, Optional


class GroupParser:
    def __init__(self, group: Optional[dict[str, Any]] = None) -> None:
        self.group: dict[str, Any] = group if isinstance(group, dict) else {}

    def get_identifiers(self) -> Any:
        return self.group.get("identifier")

    getIdentifiers = get_identifiers

    def get_active(self) -> Any:
        return self.group.get("active")

    getActive = get_active

    def get_type(self) -> Any:
        return self.group.get("type")

    getType = get_type

    def get_actual(self) -> Any:
        return self.group.get("actual")

    getActual = get_actual

    def get_code(self) -> Any:
        return self.group.get("code")

    getCode = get_code

    def get_name(self) -> Any:
        return self.group.get("name")

    getName = get_name

    def get_quantity(self) -> Any:
        return self.group.get("quantity")

    getQuantity = get_quantity

    def get_managing_entity(self) -> Any:
        return self.group.get("managingEntity")

    getManagingEntity = get_managing_entity

    def get_members(self) -> Any:
        return self.group.get("member")

    getMembers = get_members
