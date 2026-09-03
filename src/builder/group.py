from typing import Any, Dict, Optional, Union

from src.builder.base_builder import BaseBuilder


class GroupBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("Group")

    def set_meta_profile(self, profile: str) -> "GroupBuilder":
        self.data["meta/profile"] = [profile]
        return self

    def set_id(self, value: str) -> "GroupBuilder":
        return self._set("id", value)

    def add_identifier(self, identifier: Union[str, Dict[str, Any]], value: Optional[str] = None) -> "GroupBuilder":
        if isinstance(identifier, str):
            return self._push("identifier", {"system": identifier, "value": value})
        return self._push("identifier", identifier)

    def set_active(self, value: bool) -> "GroupBuilder":
        return self._set("active", value)

    def set_type(self, value: str) -> "GroupBuilder":
        return self._set("type", value)

    def set_actual(self, value: bool) -> "GroupBuilder":
        return self._set("actual", value)

    def set_code(self, code: Union[Dict[str, Any], str]) -> "GroupBuilder":
        # Support "System:Code" castable notation
        if isinstance(code, str) and ":" in code:
            from src.terminology.resolver import resolve
            return self._set("code", resolve(code))
        return self._set("code", code)

    def set_name(self, value: str) -> "GroupBuilder":
        return self._set("name", value)

    def set_quantity(self, value: int) -> "GroupBuilder":
        return self._set("quantity", value)

    def set_managing_entity(self, managing_entity: Union[Dict[str, Any], str]) -> "GroupBuilder":
        if isinstance(managing_entity, str):
            from src.terminology.resolver import resolve  # noqa: F401  (unused — plain text reference)
            return self._set("managingEntity", {"reference": managing_entity})
        return self._set("managingEntity", managing_entity)

    def add_member(
        self,
        reference: Union[Dict[str, Any], str],
        display_or_period: Any = None,
        period_or_inactive: Any = None,
        inactive: Optional[bool] = None,
    ) -> "GroupBuilder":
        member: Dict[str, Any] = {}
        if isinstance(reference, str):
            ref = self._auto_prefix(reference, "Patient")
            entity: Dict[str, Any] = {"reference": ref}
            if isinstance(display_or_period, str):
                entity["display"] = display_or_period
            member["entity"] = entity
        else:
            member["entity"] = reference

        period = None
        if isinstance(display_or_period, dict):
            period = display_or_period
        elif isinstance(period_or_inactive, dict):
            period = period_or_inactive

        inactive_val = None
        if isinstance(display_or_period, bool):
            inactive_val = display_or_period
        elif isinstance(period_or_inactive, bool):
            inactive_val = period_or_inactive
        if inactive is not None:
            inactive_val = inactive

        if period is not None:
            member["period"] = period
        if inactive_val is not None:
            member["inactive"] = inactive_val

        return self._push("member", member)

    def add_extension(self, url: str, value: Any) -> "GroupBuilder":
        extension: Dict[str, Any] = {"url": url}
        if isinstance(value, bool):
            extension["valueBoolean"] = value
        elif isinstance(value, str):
            extension["valueString"] = value
        elif isinstance(value, int):
            extension["valueInteger"] = value
        elif isinstance(value, dict):
            extension.update(value)
        return self._push("extension", extension)
