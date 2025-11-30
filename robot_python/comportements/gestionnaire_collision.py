from commande.etat_robot import EtatRobot
from navigation.facade_navigation import FacadeNavigation


class GestionnaireCollision:
    
    ACTION_RECULER = "reculer"
    ACTION_STOP = "stop"
    
    def __init__(self, navigation: FacadeNavigation):
        self._navigation = navigation
    
    def verifier_collision(self, etat: EtatRobot) -> bool:

        if self._est_en_recul(etat):
            return False
        
        if self._collision_detectee():
            self._arreter_robot(etat)
            return True
        
        return False
    
    def _est_en_recul(self, etat: EtatRobot) -> bool:
        """Vérifie si le robot est en train de reculer."""
        return etat.action_courante == self.ACTION_RECULER
    
    def _collision_detectee(self) -> bool:
        """Vérifie si une collision est détectée par les capteurs."""
        return self._navigation.verifier_collision()
    
    def _arreter_robot(self, etat: EtatRobot) -> None:
        """Arrête le robot en cas de collision."""
        etat.action_courante = self.ACTION_STOP
