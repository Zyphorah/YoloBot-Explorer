import time
from commande.etat_robot import EtatRobot
from navigation.facade_navigation import FacadeNavigation


class GestionnaireRotation:
   
    
    DUREE_ROTATION = 1.0  # Durée en secondes pour une rotation 90°
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
        """Vérifie si le robot est actuellement en rotation."""
        return etat.action_courante in self.ACTIONS_ROTATION
    
    def _rotation_terminee(self, etat: EtatRobot) -> bool:
        """Vérifie si la durée de rotation est écoulée."""
        temps_ecoule = time.time() - etat.debut_rotation
        return temps_ecoule >= self.DUREE_ROTATION
    
    def _finaliser_rotation(self, etat: EtatRobot) -> None:
        """Termine la rotation et passe en mode avancer."""
        print("Fin de rotation 90°, passage en mode AVANCER")
        self._navigation.avancer()
        etat.action_courante = "avancer"
