from typing import Optional
from commande.etat_robot import EtatRobot
from moteur.servo import Servo
from navigation.facade_navigation import FacadeNavigation
from vision.camera import Camera
from services.ble_service import BLEService


class GestionnaireAutonome:

    POSITIONS_SCAN = [0, 90, 180]
    ANGLE_MIN = 0
    ANGLE_MAX = 180
    ANGLE_ROTATION_ROUES = 30
    AJUSTEMENT_CENTRAGE = 10

    def __init__(self, servo: Servo, navigation: FacadeNavigation, camera: Camera, ble_service: BLEService):
        self._servo = servo
        self._navigation = navigation
        self._camera = camera
        self._ble = ble_service
        self._index_position = 0
        self._angle_servo_actuel = 90
        self._scan_en_cours = False
        self._cible_trouvee = False
        self._en_deplacement = False
        self._mission_complete = False

    def executer(self, etat: EtatRobot) -> bool:
        if not etat.mode_autonome:
            self._reinitialiser()
            return False

        if self._mission_complete:
            return True

        if self._cible_trouvee:
            return self._avancer_vers_cible(etat)

        if not self._scan_en_cours:
            self._demarrer_scan()

        return self._effectuer_scan(etat)

    def _demarrer_scan(self) -> None:
        print("Autonome: demarrage scan")
        self._scan_en_cours = True
        self._index_position = 0
        self._angle_servo_actuel = self.POSITIONS_SCAN[0]
        self._servo.tourner(self._angle_servo_actuel)

    def _effectuer_scan(self, etat: EtatRobot) -> bool:
        objet_detecte = self._camera.detecter_objets(etat.objet_cible)

        if objet_detecte:
            print(f"Autonome: cible {etat.objet_cible} trouvee a {self._angle_servo_actuel} degres")
            self._cible_trouvee = True
            self._aligner_robot_vers_cible()
            return False

        self._continuer_scan()
        return False

    def _aligner_robot_vers_cible(self) -> None:
        angle_rotation = 90 - self._angle_servo_actuel
        if angle_rotation > 0:
            print(f"Autonome: rotation droite de {angle_rotation} degres")
            self._navigation.tourner_angle_droit(angle_rotation)
        elif angle_rotation < 0:
            print(f"Autonome: rotation gauche de {abs(angle_rotation)} degres")
            self._navigation.tourner_angle_gauche(abs(angle_rotation))
        self._servo.tourner(90)
        self._angle_servo_actuel = 90

    def _avancer_vers_cible(self, etat: EtatRobot) -> bool:
        if self._navigation.verifier_collision():
            print("Autonome: obstacle detecte, mission complete")
            self._navigation.arreter()
            self._mission_complete = True
            self._ble.send_status(f"Mission complete: {etat.objet_cible} atteint")
            return True

        objet_detecte = self._camera.detecter_objets(etat.objet_cible)

        if not objet_detecte:
            print("Autonome: cible perdue, retour scan")
            self._navigation.arreter()
            self._cible_trouvee = False
            self._scan_en_cours = False
            return False

        position = objet_detecte.get('position')

        if position == 'gauche':
            self._ajuster_direction_gauche()
        elif position == 'droite':
            self._ajuster_direction_droite()

        if not self._en_deplacement:
            print("Autonome: avance vers cible")
            self._en_deplacement = True

        self._navigation.avancer()
        return False

    def _ajuster_direction_gauche(self) -> None:
        nouvel_angle = min(self.ANGLE_MAX, self._angle_servo_actuel + self.AJUSTEMENT_CENTRAGE)
        if nouvel_angle != self._angle_servo_actuel:
            self._angle_servo_actuel = nouvel_angle
            self._servo.tourner(self._angle_servo_actuel)
            if self._angle_servo_actuel >= 110:
                print("Autonome: correction trajectoire gauche")
                self._navigation.tourner_angle_gauche(10)
                self._servo.tourner(90)
                self._angle_servo_actuel = 90

    def _ajuster_direction_droite(self) -> None:
        nouvel_angle = max(self.ANGLE_MIN, self._angle_servo_actuel - self.AJUSTEMENT_CENTRAGE)
        if nouvel_angle != self._angle_servo_actuel:
            self._angle_servo_actuel = nouvel_angle
            self._servo.tourner(self._angle_servo_actuel)
            if self._angle_servo_actuel <= 70:
                print("Autonome: correction trajectoire droite")
                self._navigation.tourner_angle_droit(10)
                self._servo.tourner(90)
                self._angle_servo_actuel = 90

    def _continuer_scan(self) -> None:
        self._index_position += 1

        if self._index_position >= len(self.POSITIONS_SCAN):
            print(f"Autonome: scan complet, rotation {self.ANGLE_ROTATION_ROUES} degres")
            self._navigation.tourner_angle_droit(self.ANGLE_ROTATION_ROUES)
            self._index_position = 0
            self._angle_servo_actuel = self.POSITIONS_SCAN[0]
            self._servo.tourner(self._angle_servo_actuel)
            return

        self._angle_servo_actuel = self.POSITIONS_SCAN[self._index_position]
        self._servo.tourner(self._angle_servo_actuel)
        print(f"Autonome: scan a {self._angle_servo_actuel} degres")

    def _reinitialiser(self) -> None:
        if self._scan_en_cours or self._en_deplacement:
            print("Autonome: arret")
            self._navigation.arreter()
        self._scan_en_cours = False
        self._cible_trouvee = False
        self._en_deplacement = False
        self._mission_complete = False
        self._index_position = 0
        self._angle_servo_actuel = 90

    def forcer_arret(self) -> None:
        self._reinitialiser()
        self._servo.tourner(90)

    def est_mission_complete(self) -> bool:
        return self._mission_complete

    def relancer_mission(self) -> None:
        self._mission_complete = False
        self._cible_trouvee = False
        self._scan_en_cours = False
        self._en_deplacement = False
