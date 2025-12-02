from abc import ABC, abstractmethod

class ICommande(ABC):
    @abstractmethod
    def executer(self) -> dict:
        pass
