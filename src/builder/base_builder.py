from typing import Any, Dict, List

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

    def build(self) -> Dict[str, Any]:
        return self.data

    def to_array(self) -> Dict[str, Any]:
        return self.build()
