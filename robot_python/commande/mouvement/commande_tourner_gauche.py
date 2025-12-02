import time
from commande.interfaces.i_commande import ICommande


class CommandeTournerGauche(ICommande):
    
    def __init__(self, navigation):
        self.navigation = navigation
    
    def executer(self) -> dict:
        self.navigation.tourner_gauche()
        return {
            "action_courante": "tourner_gauche_90",
            "debut_rotation": time.time()
        }
