from commande.etat_robot import EtatRobot
from navigation.facade_navigation import FacadeNavigation
from vision.camera import Camera
from services.ble_service import BLEService
from moteur.servo import Servo


class GestionnaireAutonome:

    def __init__(self, servo: Servo, navigation: FacadeNavigation, camera: Camera, ble_service: BLEService):
        self._servo = servo
        self._navigation = navigation
        self._camera = camera
        self._ble = ble_service
        self._angle_servo = 90
        self._mission_complete = False
        self._en_approche = False

    def executer(self, etat: EtatRobot) -> bool:
        if not etat.mode_autonome:
            self._reinitialiser()
            return False

        if self._mission_complete:
            return True

        if self._navigation.verifier_collision():
            return self._terminer_mission(etat)

        objet = self._camera.detecter_objets(etat.objet_cible)
        
        if not objet:
            return self._chercher_cible()

        return self._approcher_cible(objet)

    def _chercher_cible(self) -> bool:
        if self._en_approche:
            print("Autonome: cible perdue, recherche")
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
        position = objet.get('position')
        boite = objet.get('boite', [0, 0, 0, 0])
        centre_x = (boite[0] + boite[2]) // 2
        largeur_image = 640
        
        offset_pixel = centre_x - (largeur_image // 2)
        offset_degres = (offset_pixel / largeur_image) * 60
        
        angle_reel = self._angle_servo - 90 + offset_degres
        
        if abs(angle_reel) > 5:
            self._aligner_vers_cible(angle_reel)
            return False
        
        if not self._en_approche:
            print("Autonome: cible alignee, avance")
            self._en_approche = True
        
        self._navigation.avancer()
        return False

    def _aligner_vers_cible(self, angle: float) -> None:
        self._navigation.arreter()
        
        if angle > 0:
            print(f"Autonome: rotation gauche {abs(angle):.0f} degres")
            self._navigation.tourner_angle_gauche(abs(angle))
        else:
            print(f"Autonome: rotation droite {abs(angle):.0f} degres")
            self._navigation.tourner_angle_droit(abs(angle))
        
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

    def forcer_arret(self) -> None:
        self._reinitialiser()
        self._servo.tourner(90)

    def relancer_mission(self) -> None:
        self._mission_complete = False
        self._en_approche = False
        self._angle_servo = 90
        self._servo.tourner(90)
