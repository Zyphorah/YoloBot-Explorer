from abc import ABC, abstractmethod

class ICleanup(ABC):
    @abstractmethod
    def cleanup(self):
        pass
