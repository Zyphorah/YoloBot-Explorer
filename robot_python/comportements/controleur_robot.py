from commande.etat_robot import EtatRobot
from commande import CommandHandler
from services.ble_service import BLEService
from navigation.facade_navigation import FacadeNavigation
from moteur.servo import Servo
from vision.camera import Camera

from comportements.comportement_autonome import ComportementAutonome
from comportements.gestionnaire_rotation import GestionnaireRotation
from comportements.gestionnaire_collision import GestionnaireCollision
from comportements.gestionnaire_detection import GestionnaireDetection

class ControleurRobot:
    def __init__(
        self,
        navigation: FacadeNavigation,
        servo: Servo,
        camera: Camera,
        ble_service: BLEService
    ):
     
        self._navigation = navigation
        self._servo = servo
        self._ble = ble_service
        
        # État centralisé du robot
        self._etat = EtatRobot()
        
        # Handler de commandes (patron Commande)
        self._command_handler = CommandHandler(navigation, servo)
        
        # Gestionnaires de comportements
        self._detection = GestionnaireDetection(camera, ble_service)
        self._autonome = ComportementAutonome(navigation)
        self._rotation = GestionnaireRotation(navigation)
        self._collision = GestionnaireCollision(navigation)
    
    def initialiser(self) -> None:
        """Initialise le robot (position par défaut)."""
        self._servo.tourner(90)  # Caméra centrée
        print(f"Commandes disponibles : {self._command_handler.lister_commandes()}")
    
    def executer_cycle(self) -> None:

        self._traiter_commande_bluetooth()
        self._traiter_detection()
        self._rotation.verifier_et_terminer_rotation(self._etat)
        self._collision.verifier_collision(self._etat)
    
    def _traiter_commande_bluetooth(self) -> None:
        """Traite les commandes Bluetooth entrantes."""
        commande = self._ble.obtenir_derniere_commande()
        
        if commande:
            changements = self._command_handler.executer_commande(commande)
            self._etat.appliquer_changements(changements)
    
    def _traiter_detection(self) -> None:
        """Traite la détection d'objets et le comportement autonome."""
        objet_detecte = self._detection.detecter(self._etat)
        
        if objet_detecte:
            self._autonome.executer(self._etat, objet_detecte)
    
    def nettoyer(self) -> None:
        print("Nettoyage des ressources...")
        
        self._ble.stop()
        self._navigation.cleanup()
        self._detection.liberer()
        
        print("Terminé.")
    
    @property
    def etat(self) -> EtatRobot:
        """Retourne l'état actuel du robot."""
        return self._etat
