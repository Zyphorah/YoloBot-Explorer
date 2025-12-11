from typing import Optional
from commande.etat_robot import EtatRobot
from vision.camera import Camera
from services.ble_service import BLEService


class GestionnaireDetection:
    
    def __init__(self, camera: Camera, ble_service: BLEService):
        self._camera = camera
        self._ble = ble_service
    
    def detecter(self, etat: EtatRobot) -> Optional[dict]:
        if not self._detection_active(etat):
            return None
        
        couleur_cible = getattr(etat, 'couleur_cible', None)
        objet_detecte = self._camera.detecter_objets(etat.objet_cible, couleur_cible)
        
        if objet_detecte:
            self._notifier_detection(objet_detecte)
        
        return objet_detecte
    
    def _detection_active(self, etat: EtatRobot) -> bool:
        return etat.mode_detection or etat.mode_autonome
    
    def _notifier_detection(self, objet_detecte: dict) -> None:
        couleur = objet_detecte.get('couleur', '')
        couleur_str = f" {couleur}" if couleur else ""
        msg = f"Detection: {objet_detecte['classe']}{couleur_str} ({objet_detecte['position']})"
        print(msg)
        self._ble.send_status(msg)
    
    def liberer(self) -> None:
        print("Detection: liberation camera")
        try:
            self._camera.release()
        except Exception:
            pass
