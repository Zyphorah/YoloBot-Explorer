from typing import Optional
from commande.etat_robot import EtatRobot
from moteur.servo import Servo
from navigation.facade_navigation import FacadeNavigation
from vision.camera import Camera
from services.ble_service import BLEService

class GestionnaireScanDetection:

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
        self._angle_servo_actuel = 0
        self._scan_en_cours = False
        self._mode_suivi = False
    
    def executer(self, etat: EtatRobot) -> Optional[dict]:
        if not etat.mode_detection:
            self._reinitialiser_scan()
            return None
        
        if self._mode_suivi:
            return self._suivre_cible(etat)
        
        if not self._scan_en_cours:
            self._demarrer_scan()
        
        return self._effectuer_etape_scan(etat)
    
    def _demarrer_scan(self) -> None:
        print("Scan: demarrage")
        self._scan_en_cours = True
        self._mode_suivi = False
        self._index_position = 0
        self._angle_servo_actuel = self.POSITIONS_SCAN[0]
        self._servo.tourner(self._angle_servo_actuel)
    
    def _effectuer_etape_scan(self, etat: EtatRobot) -> Optional[dict]:
        objet_detecte = self._camera.detecter_objets(etat.objet_cible)
        
        if objet_detecte:
            print(f"Scan: cible trouvee a {self._angle_servo_actuel} degres")
            self._mode_suivi = True
            self._centrer_cible_avec_servo(objet_detecte.get('position'))
            return objet_detecte
        
        self._continuer_scan()
        return None
    
    def _suivre_cible(self, etat: EtatRobot) -> Optional[dict]:
        objet_detecte = self._camera.detecter_objets(etat.objet_cible)
        
        if objet_detecte:
            self._centrer_cible_avec_servo(objet_detecte.get('position'))
            return objet_detecte
        
        print("Scan: cible perdue, retour en mode scan")
        self._mode_suivi = False
        self._scan_en_cours = False
        return None
    
    def _centrer_cible_avec_servo(self, position: str) -> None:
        if position == 'gauche':
            nouvel_angle = min(self.ANGLE_MAX, self._angle_servo_actuel + self.AJUSTEMENT_CENTRAGE)
            if nouvel_angle != self._angle_servo_actuel:
                self._angle_servo_actuel = nouvel_angle
                self._servo.tourner(self._angle_servo_actuel)
                print(f"Scan: servo ajuste a {self._angle_servo_actuel} degres (gauche)")
        elif position == 'droite':
            nouvel_angle = max(self.ANGLE_MIN, self._angle_servo_actuel - self.AJUSTEMENT_CENTRAGE)
            if nouvel_angle != self._angle_servo_actuel:
                self._angle_servo_actuel = nouvel_angle
                self._servo.tourner(self._angle_servo_actuel)
                print(f"Scan: servo ajuste a {self._angle_servo_actuel} degres (droite)")
    
    def _continuer_scan(self) -> None:
        self._index_position += 1
        
        if self._index_position >= len(self.POSITIONS_SCAN):
            print(f"Scan: complet sans cible, rotation roues de {self.ANGLE_ROTATION_ROUES} degres")
            self._navigation.tourner_angle_droit(self.ANGLE_ROTATION_ROUES)
            self._index_position = 0
            self._angle_servo_actuel = self.POSITIONS_SCAN[0]
            self._servo.tourner(self._angle_servo_actuel)
            return
        
        self._angle_servo_actuel = self.POSITIONS_SCAN[self._index_position]
        self._servo.tourner(self._angle_servo_actuel)
        print(f"Scan: servo a {self._angle_servo_actuel} degres")
    
    def _reinitialiser_scan(self) -> None:
        if self._scan_en_cours:
            print("Scan: arret")
        self._scan_en_cours = False
        self._mode_suivi = False
        self._index_position = 0
        self._angle_servo_actuel = self.POSITIONS_SCAN[0]
    
    def forcer_arret_scan(self) -> None:
        self._reinitialiser_scan()
        self._servo.tourner(90)
