from abc import ABC, abstractmethod

class i_direction(ABC):
    @abstractmethod
    def avancer(self):
        pass

    @abstractmethod
    def reculer(self): 
        pass

    @abstractmethod
    def arreter(self):
        pass

    @abstractmethod
    def cleanup():
        pass
