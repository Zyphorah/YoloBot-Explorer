from commande.etat_robot import EtatRobot
from navigation.facade_navigation import FacadeNavigation


class ComportementAutonome:
    """
    Comportement de navigation autonome vers un objet détecté.
    Ajuste la direction du robot en fonction de la position de l'objet dans l'image.
    """

    ANGLE_AJUSTEMENT_GRAND = 20
    ANGLE_AJUSTEMENT_MOYEN = 12
    ANGLE_AJUSTEMENT_PETIT = 6
    
    def __init__(self, navigation: FacadeNavigation):
        self._navigation = navigation
    
    def executer(self, etat: EtatRobot, objet_detecte: dict) -> None:
        """
        Exécute le comportement autonome basé sur la détection d'objet.
        
        Args:
            etat: État actuel du robot
            objet_detecte: Dictionnaire contenant les infos de détection
        """
        if not etat.mode_autonome or not objet_detecte:
            return
        
        position = objet_detecte.get('position')
        boite = objet_detecte.get('boite', [0, 0, 0, 0])
        
        # Calculer le décalage précis pour ajuster l'angle
        centre_x = (boite[0] + boite[2]) // 2
        largeur_image = 640
        decalage = abs(centre_x - largeur_image // 2)
        
        # Choisir l'angle d'ajustement en fonction du décalage
        if decalage > 200:
            angle = self.ANGLE_AJUSTEMENT_GRAND
        elif decalage > 100:
            angle = self.ANGLE_AJUSTEMENT_MOYEN
        else:
            angle = self.ANGLE_AJUSTEMENT_PETIT
        
        if position == 'gauche':
            self._ajuster_gauche(etat, angle)
        elif position == 'droite':
            self._ajuster_droite(etat, angle)
        elif position == 'centre':
            self._objet_centre(etat, objet_detecte)
    
    def _ajuster_gauche(self, etat: EtatRobot, angle: int) -> None:
        print(f"Autonome: ajustement gauche de {angle} degres")
        self._navigation.tourner_angle_gauche(angle)
        self._continuer_avancer(etat)
    
    def _ajuster_droite(self, etat: EtatRobot, angle: int) -> None:
        print(f"Autonome: ajustement droite de {angle} degres")
        self._navigation.tourner_angle_droit(angle)
        self._continuer_avancer(etat)
    
    def _objet_centre(self, etat: EtatRobot, objet_detecte: dict) -> None:
        """Quand l'objet est centré, avancer vers lui"""
        print("Autonome: objet centre, avance vers la cible")
        self._navigation.avancer()
    
    def _continuer_avancer(self, etat: EtatRobot) -> None:
        """Continue à avancer après un ajustement de direction"""
        self._navigation.avancer()
