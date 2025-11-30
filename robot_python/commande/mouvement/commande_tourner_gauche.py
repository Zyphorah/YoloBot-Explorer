import time
from commande.interfaces.i_commande import ICommande


class CommandeTournerGauche(ICommande):
    """Commande pour tourner à gauche (90°)."""
    
    def __init__(self, navigation):
        self.navigation = navigation
    
    def executer(self) -> dict:
        self.navigation.tourner_gauche()
        return {
            "action_courante": "tourner_gauche_90",
            "debut_rotation": time.time()
        }
    
    def get_nom(self) -> str:
        return "gauche"
