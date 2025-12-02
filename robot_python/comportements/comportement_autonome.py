from commande.etat_robot import EtatRobot
from navigation.facade_navigation import FacadeNavigation


class ComportementAutonome:

    ANGLE_AJUSTEMENT = 15
    
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
        print(f"Autonome: ajustement gauche de {self.ANGLE_AJUSTEMENT} degres")
        self._navigation.tourner_angle_gauche(self.ANGLE_AJUSTEMENT)
        self._continuer_avancer_si_necessaire(etat)
    
    def _ajuster_droite(self, etat: EtatRobot) -> None:
        print(f"Autonome: ajustement droite de {self.ANGLE_AJUSTEMENT} degres")
        self._navigation.tourner_angle_droit(self.ANGLE_AJUSTEMENT)
        self._continuer_avancer_si_necessaire(etat)
    
    def _objet_centre(self, etat: EtatRobot) -> None:
        pass
    
    def _continuer_avancer_si_necessaire(self, etat: EtatRobot) -> None:
        if etat.action_courante == "avancer":
            self._navigation.avancer()
