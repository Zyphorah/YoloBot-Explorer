import os

from services.ble_service import BLEService
from navigation.facade_navigation import FacadeNavigation
from moteur.servo import Servo
from vision.camera import Camera
from comportements import ControleurRobot

def creer_camera() -> Camera:
    """Crée et configure l'instance de la caméra."""
    model_path = "../yolov8n.pt"
    if not os.path.exists(model_path):
        model_path = "yolov8n.pt"
    
    print(f"Chargement du modèle IA depuis {model_path}...")
    return Camera(model_path)

def main():
    """Point d'entrée principal du robot."""
    print("--- Initialisation du Robot ---")
    
    # Création des instances
    camera = creer_camera()
    ble = BLEService()
    nav = FacadeNavigation()
    servo = Servo()
    
    # Démarrage du Bluetooth
    ble.start()
    print("Service BLE démarré.")
    
    # Création du contrôleur principal
    controleur = ControleurRobot(nav, servo, camera, ble)
    controleur.initialiser()
    
    print("--- Robot Prêt ---")
    print("En attente de commandes BLE ou de détection...")
    
    try:
        # Boucle principale
        while True:
            controleur.executer_cycle()
    
    except KeyboardInterrupt:
        print("\nArrêt du programme...")
    except Exception as e:
        print(f"\nErreur inattendue : {e}")
    finally:
        controleur.nettoyer()

if __name__ == "__main__":
    main()

