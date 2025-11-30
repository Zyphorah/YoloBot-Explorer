from commande.etat_robot import EtatRobot
from navigation.facade_navigation import FacadeNavigation


class ComportementAutonome:

    ANGLE_AJUSTEMENT = 15  # Degrés de rotation pour l'ajustement
    
    def __init__(self, navigation: FacadeNavigation):
 
        self._navigation = navigation
    
    def executer(self, etat: EtatRobot, objet_detecte: dict) -> None:
 
        if not etat.mode_autonome or not objet_detecte:
            return
        
        position = objet_detecte.get('position')
        
        if position == 'gauche':
            self._ajuster_gauche(etat)
        elif position == 'droite':
            self._ajuster_droite(etat)
        elif position == 'centre':
            self._objet_centre(etat)
    
    def _ajuster_gauche(self, etat: EtatRobot) -> None:
        """Ajuste la trajectoire vers la gauche."""
        self._navigation.tourner_angle_gauche(self.ANGLE_AJUSTEMENT)
        self._continuer_avancer_si_necessaire(etat)
    
    def _ajuster_droite(self, etat: EtatRobot) -> None:
        """Ajuste la trajectoire vers la droite."""
        self._navigation.tourner_angle_droit(self.ANGLE_AJUSTEMENT)
        self._continuer_avancer_si_necessaire(etat)
    
    def _objet_centre(self, etat: EtatRobot) -> None:
        """L'objet est au centre, on peut continuer tout droit."""
        # Pour l'instant, on ne fait rien quand l'objet est centré
        # On pourrait ajouter une logique pour avancer vers l'objet
        pass
    
    def _continuer_avancer_si_necessaire(self, etat: EtatRobot) -> None:
        """Continue à avancer si le robot était déjà en mouvement."""
        if etat.action_courante == "avancer":
            self._navigation.avancer()
