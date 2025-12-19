import time
from commande.etat_robot import EtatRobot
from navigation.facade_navigation import FacadeNavigation


class GestionnaireRotation:
    
    DUREE_ROTATION = 1.5
    ACTIONS_ROTATION = ["tourner_gauche_90", "tourner_droite_90"]
    
    def __init__(self, navigation: FacadeNavigation):
        self._navigation = navigation
    
    def verifier_et_terminer_rotation(self, etat: EtatRobot) -> bool:
        if not self._est_en_rotation(etat):
            return False
        
        if self._rotation_terminee(etat):
            self._finaliser_rotation(etat)
            return True
        
        return False
    
    def _est_en_rotation(self, etat: EtatRobot) -> bool:
        return etat.action_courante in self.ACTIONS_ROTATION
    
    def _rotation_terminee(self, etat: EtatRobot) -> bool:
        temps_ecoule = time.time() - etat.debut_rotation
        return temps_ecoule >= self.DUREE_ROTATION
    
    def _finaliser_rotation(self, etat: EtatRobot) -> None:
        print("Rotation: fin de rotation 90 degres, passage en mode avancer")
        self._navigation.avancer()
        etat.action_courante = "avancer"
