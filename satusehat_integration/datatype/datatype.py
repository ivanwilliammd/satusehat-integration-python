from abc import ABC, abstractmethod

class DataType(ABC):
    @abstractmethod
    def to_array(self) -> dict:
        pass
