from abc import ABC, abstractmethod

class IRotation_angle(ABC):
    
    @abstractmethod
    def tourner(self, angle):
        pass
