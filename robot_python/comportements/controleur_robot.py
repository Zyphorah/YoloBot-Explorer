from commande.etat_robot import EtatRobot
from commande import CommandHandler
from services.ble_service import BLEService
from navigation.facade_navigation import FacadeNavigation
from moteur.servo import Servo
from vision.camera import Camera

from comportements.gestionnaire_rotation import GestionnaireRotation
from comportements.gestionnaire_collision import GestionnaireCollision
from comportements.gestionnaire_detection import GestionnaireDetection
from comportements.gestionnaire_scan_detection import GestionnaireScanDetection
from comportements.gestionnaire_autonome import GestionnaireAutonome

class ControleurRobot:
    def __init__(self, navigation: FacadeNavigation, servo: Servo, camera: Camera, ble_service: BLEService):
        self._navigation = navigation
        self._servo = servo
        self._ble = ble_service
        self._camera = camera
        self._etat = EtatRobot()
        self._command_handler = CommandHandler(navigation, servo)
        self._detection = GestionnaireDetection(camera, ble_service)
        self._scan_detection = GestionnaireScanDetection(servo, navigation, camera, ble_service)
        self._autonome = GestionnaireAutonome(servo, navigation, camera, ble_service)
        self._rotation = GestionnaireRotation(navigation)
        self._collision = GestionnaireCollision(navigation)
     
    def initialiser(self) -> None:
        self._servo.tourner(90)
        print(f"Robot: initialise, commandes: {self._command_handler.lister_commandes()}")

    def executer_cycle(self) -> None:
        self._traiter_commande_bluetooth()
        
        if self._etat.mode_autonome:
            self._traiter_mode_autonome()
        elif self._etat.mode_detection:
            self._traiter_scan_detection()
        else:
            self._collision.verifier_collision(self._etat)
        
        self._rotation.verifier_et_terminer_rotation(self._etat)

    def _traiter_commande_bluetooth(self) -> None:
        commande = self._ble.obtenir_derniere_commande()
        if commande:
            print(f"Robot: commande: {commande}")
            changements = self._command_handler.executer_commande(commande)
            self._etat.appliquer_changements(changements)
            if "mode_autonome" in changements and changements["mode_autonome"]:
                self._autonome.relancer_mission()

    def _traiter_mode_autonome(self) -> None:
        self._autonome.executer(self._etat)

    def _traiter_scan_detection(self) -> None:
        self._scan_detection.executer(self._etat)

    def nettoyer(self) -> None:
        print("Robot: nettoyage")
        self._scan_detection.forcer_arret_scan()
        self._autonome.forcer_arret()
        self._ble.stop()
        self._navigation.cleanup()
        self._detection.liberer()
        print("Robot: termine")

    @property
    def etat(self) -> EtatRobot:
        return self._etat
