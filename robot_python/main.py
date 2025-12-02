import os

from services.ble_service import BLEService
from navigation.facade_navigation import FacadeNavigation
from moteur.servo import Servo
from vision.camera import Camera
from comportements import ControleurRobot

def creer_camera() -> Camera:
    model_path = "../yolov8n.pt"
    if not os.path.exists(model_path):
        model_path = "yolov8n.pt"
    print(f"Main: chargement modele IA depuis {model_path}")
    return Camera(model_path)

def main():
    print("Main: initialisation du robot")
    
    camera = creer_camera()
    ble = BLEService()
    nav = FacadeNavigation()
    servo = Servo()
    
    ble.start()
    
    controleur = ControleurRobot(nav, servo, camera, ble)
    controleur.initialiser()
    
    print("Main: robot pret, en attente de commandes")
    
    try:
        while True:
            controleur.executer_cycle()
    except KeyboardInterrupt:
        print("Main: arret du programme")
    except Exception as e:
        print(f"Main: erreur inattendue: {e}")
    finally:
        controleur.nettoyer()

if __name__ == "__main__":
    main()

