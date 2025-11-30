from abc import ABC, abstractmethod


class ICommande(ABC):
    """Interface abstraite pour le patron de conception Commande."""
    
    @abstractmethod
    def executer(self) -> dict:
        """
        Exécute la commande.
        
        Returns:
            dict: Dictionnaire contenant les changements d'état à appliquer.
                  Ex: {"action_courante": "avancer", "mode_autonome": True}
        """
        pass
    
    @abstractmethod
    def get_nom(self) -> str:
        """Retourne le nom de la commande pour le matching."""
        pass
