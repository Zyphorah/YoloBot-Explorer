from abc import ABC, abstractmethod

class IRotation(ABC):
    @abstractmethod
    def tourner_droite(self):
        pass

    @abstractmethod
    def tourner_gauche(self): 
        pass

    @abstractmethod
    def arreter(self):
        pass
