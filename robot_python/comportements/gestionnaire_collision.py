from commande.etat_robot import EtatRobot
from navigation.facade_navigation import FacadeNavigation


class GestionnaireCollision:
    
    ACTION_RECULER = "reculer"
    
    def __init__(self, navigation: FacadeNavigation):
        self._navigation = navigation
    
    def verifier_collision(self, etat: EtatRobot) -> bool:
        if etat.action_courante == self.ACTION_RECULER:
            return False
        
        if self._navigation.verifier_collision():
            print("Collision: detectee, arret des moteurs")
            return True
        
        return False
