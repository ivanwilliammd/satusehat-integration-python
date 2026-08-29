from typing import Any, Dict


class BaseBuilder:
    def __init__(self, resource_type: str):
        self.data: Dict[str, Any] = {"resourceType": resource_type}

    def to_array(self) -> Dict[str, Any]:
        return self.data
