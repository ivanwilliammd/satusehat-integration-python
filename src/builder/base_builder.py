from typing import Any, Dict


class BaseBuilder:
    def __init__(self, resource_type: str):
        self.data: Dict[str, Any] = {"resourceType": resource_type}

    def _set(self, key: str, value: Any) -> "BaseBuilder":
        if value is not None and value != "" and value != [] and value != {}:
            self.data[key] = value
        return self

    def _push(self, key: str, value: Any) -> "BaseBuilder":
        if key not in self.data:
            self.data[key] = []
        if isinstance(self.data[key], list):
            self.data[key].append(value)
        return self

    def _append(self, key: str, value: Any) -> "BaseBuilder":
        return self._push(key, value)

    def _auto_prefix(self, ref: str, resource_type: str) -> str:
        """Auto-prefix bare reference with resource type if no urn:/http(s):// or / present."""
        if not ref.startswith(("urn:", "http://", "https://")) and "/" not in ref:
            return f"{resource_type}/{ref}"
        return ref

    def _ref(self, ref: str, resource_type: str, display: str = None) -> Dict[str, Any]:
        """Build a Reference dict with auto-prefix."""
        result: Dict[str, Any] = {"reference": self._auto_prefix(ref, resource_type)}
        if display:
            result["display"] = display
        return result

    def build(self) -> Dict[str, Any]:
        return {k: v for k, v in self.data.items() if v not in (None, "", [], {})}

    def to_array(self) -> Dict[str, Any]:
        return self.build()
