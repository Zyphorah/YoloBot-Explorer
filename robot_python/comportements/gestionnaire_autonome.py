from commande.etat_robot import EtatRobot
from navigation.facade_navigation import FacadeNavigation
from vision.camera import Camera
from services.ble_service import BLEService
from moteur.servo import Servo


class GestionnaireAutonome:

    SEUIL_TRES_PROCHE = 0.6
    SEUIL_PROCHE = 0.3
    SEUIL_ALIGNEMENT = 10
    
    def __init__(self, servo: Servo, navigation: FacadeNavigation, camera: Camera, ble_service: BLEService):
        self._servo = servo
        self._navigation = navigation
        self._camera = camera
        self._ble = ble_service
        self._angle_servo = 90
        self._mission_complete = False
        self._en_approche = False
        self._compteur_perdu = 0

    def executer(self, etat: EtatRobot) -> bool:
        if not etat.mode_autonome:
            self._reinitialiser()
            return False

        if self._mission_complete:
            return True

        if self._navigation.verifier_collision():
            return self._terminer_mission(etat)

        couleur_cible = getattr(etat, 'couleur_cible', None)
        objet = self._camera.detecter_objets(etat.objet_cible, couleur_cible)
        
        if not objet:
            return self._chercher_cible()

        return self._approcher_cible(objet)

    def _chercher_cible(self) -> bool:
        self._compteur_perdu += 1
        
        if self._en_approche and self._compteur_perdu < 3:
            print(f"Autonome: cible temporairement perdue ({self._compteur_perdu}/3), continue")
            return False
        
        if self._en_approche:
            print("Autonome: cible perdue, arret et recherche")
            self._navigation.arreter()
            self._en_approche = False
        
        self._scanner_environnement()
        return False

    def _scanner_environnement(self) -> None:
        positions = [0, 45, 90, 135, 180]
        idx = positions.index(self._angle_servo) if self._angle_servo in positions else 2
        idx = (idx + 1) % len(positions)
        self._angle_servo = positions[idx]
        self._servo.tourner(self._angle_servo)

    def _approcher_cible(self, objet: dict) -> bool:
        # Réinitialiser le compteur de perte de cible
        self._compteur_perdu = 0
        
        boite = objet.get('boite', [0, 0, 0, 0])
        x1, y1, x2, y2 = boite
        centre_x = (x1 + x2) // 2
        hauteur_boite = y2 - y1
        largeur_image = 640
        hauteur_image = 640
        
        # Calculer le ratio de taille pour estimer la distance
        ratio_taille = hauteur_boite / hauteur_image
        
        # Calculer l'offset en degrés pour l'alignement
        offset_pixel = centre_x - (largeur_image // 2)
        offset_degres = (offset_pixel / largeur_image) * 60
        
        angle_reel = self._angle_servo - 90 + offset_degres
        
        # Vérifier si on est très proche de la cible
        if ratio_taille >= self.SEUIL_TRES_PROCHE:
            print(f"Autonome: cible tres proche (taille={ratio_taille:.0%})")
            return self._approche_finale(objet)
        
        if abs(angle_reel) > self.SEUIL_ALIGNEMENT:
            self._aligner_vers_cible(angle_reel)
            return False
        
        # Cible alignée, avancer
        if not self._en_approche:
            couleur = objet.get('couleur', '')
            classe = objet.get('classe', 'objet')
            print(f"Autonome: {classe} {couleur} aligne (taille={ratio_taille:.0%}), avance")
            self._en_approche = True
        
        self._navigation.avancer()
        return False
    
    def _approche_finale(self, objet: dict) -> bool:
        """Gère l'approche finale quand on est très proche de la cible"""
        boite = objet.get('boite', [0, 0, 0, 0])
        x1, y1, x2, y2 = boite
        centre_x = (x1 + x2) // 2
        largeur_image = 640
        
        # Petit ajustement si la cible n'est pas centrée
        offset_pixel = centre_x - (largeur_image // 2)
        
        if abs(offset_pixel) > 80:  # Seuil plus large pour l'approche finale
            # Micro-ajustement de direction
            if offset_pixel > 0:
                print("Autonome: micro-ajustement droite")
                self._navigation.tourner_angle_droit(5)
            else:
                print("Autonome: micro-ajustement gauche")
                self._navigation.tourner_angle_gauche(5)
        
        # Continuer à avancer doucement vers la cible
        self._navigation.avancer()
        return False

    def _aligner_vers_cible(self, angle: float) -> None:
        self._navigation.arreter()
        
        angle_abs = abs(angle)
        
        if angle_abs > 45:
            angle_ajuste = angle_abs * 0.4
        elif angle_abs > 20:
            angle_ajuste = angle_abs * 0.3
        else:
            angle_ajuste = angle_abs * 0.5
        
        angle_ajuste = max(5, min(angle_ajuste, 45))
        
        if angle > 0:
            print(f"Autonome: rotation gauche {angle_ajuste:.0f} degres (ecart={angle:.0f})")
            self._navigation.tourner_angle_gauche(angle_ajuste)
        else:
            print(f"Autonome: rotation droite {angle_ajuste:.0f} degres (ecart={angle:.0f})")
            self._navigation.tourner_angle_droit(angle_ajuste)
        
        self._servo.tourner(90)
        self._angle_servo = 90
        self._en_approche = False

    def _terminer_mission(self, etat: EtatRobot) -> bool:
        print("Autonome: cible atteinte")
        self._navigation.arreter()
        self._mission_complete = True
        self._ble.send_status(f"Mission complete: {etat.objet_cible} atteint")
        return True

    def _reinitialiser(self) -> None:
        if self._en_approche:
            self._navigation.arreter()
        self._en_approche = False
        self._mission_complete = False
        self._angle_servo = 90
        self._compteur_perdu = 0

    def forcer_arret(self) -> None:
        self._reinitialiser()
        self._servo.tourner(90)

    def relancer_mission(self) -> None:
        print("Autonome: relance de la mission")
        self._mission_complete = False
        self._en_approche = False
        self._angle_servo = 90
        self._compteur_perdu = 0
        self._servo.tourner(90)
