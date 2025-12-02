import time
from commande.interfaces.i_commande import ICommande


class CommandeTournerDroite(ICommande):
    
    def __init__(self, navigation):
        self.navigation = navigation
    
    def executer(self) -> dict:
        self.navigation.tourner_droite()
        return {
            "action_courante": "tourner_droite_90",
            "debut_rotation": time.time()
        }
