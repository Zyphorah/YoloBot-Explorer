import os
import time

# Imports des modules du projet
from services.ble_service import BLEService
from navigation.facade_navigation import FacadeNavigation
from moteur.servo import Servo
from vision.camera import Camera

def main():
    print("--- Initialisation du Robot ---")

    # 1. Initialisation du Bluetooth
    ble = BLEService()
    ble.start()
    print("Service BLE démarré.")

    # 2. Initialisation de la Navigation et du Servo
    nav = FacadeNavigation()
    servo_camera = Servo()
    servo_camera.tourner(90) # Position centrale par défaut

    # 3. Initialisation de la Caméra
    # On cherche le modèle YOLO (soit dans le dossier courant, soit au-dessus)
    model_path = "../yolov8n.pt"
    if not os.path.exists(model_path):
        model_path = "yolov8n.pt"
    
    print(f"Chargement du modèle IA depuis {model_path}...")
    try:
        camera = Camera(model_path)
    except Exception as e:
        print(f"Erreur caméra: {e}")
        return

    print("--- Robot Prêt ---")
    print("En attente de commandes BLE ou de détection...")

    # Variables d'état
    mode_detection = False
    mode_autonome = False

    try:
        while True:
            # --- A. GESTION BLUETOOTH ---
            commande = ble.obtenir_derniere_commande()
            
            if commande:
                print(f"[BLE] Commande reçue : {commande}")
                
                # Logique de mouvement simple
                if "avancer" in commande:
                    # Attention : votre méthode avancer() actuelle est bloquante (boucle while)
                    # Cela mettra en pause la caméra tant que le robot avance.
                    nav.avancer() 
                elif "reculer" in commande:
                    nav.reculer()
                    time.sleep(1)
                    nav.arreter()
                elif "gauche" in commande:
                    nav.tourner_angle_gauche(90)
                elif "droite" in commande:
                    nav.tourner_angle_droit(90)
                elif "stop" in commande:
                    nav.arreter()
                    mode_autonome = False # Stop désactive aussi le mode autonome
                
                # Commandes Servo Caméra
                elif "cam_gauche" in commande:
                    servo_camera.tourner(180)
                elif "cam_droite" in commande:
                    servo_camera.tourner(0)
                elif "cam_centre" in commande:
                    servo_camera.tourner(90)

                # Commandes Modes
                elif "detect_on" in commande:
                    mode_detection = True
                    print("Mode Détection ACTIVÉ")
                elif "detect_off" in commande:
                    mode_detection = False
                    print("Mode Détection DÉSACTIVÉ")
                elif "auto_on" in commande:
                    mode_autonome = True
                    print("Mode Autonome ACTIVÉ")
                elif "auto_off" in commande:
                    mode_autonome = False
                    nav.arreter()
                    print("Mode Autonome DÉSACTIVÉ")

            # --- B. GESTION CAMÉRA ---
            if mode_detection or mode_autonome:
                # On cherche une personne (ou changez pour "bottle", "cell phone", etc.)
                objet_detecte = camera.detecter_objets("person")

                if objet_detecte:
                    msg = f"Vu: {objet_detecte['classe']} ({objet_detecte['position']})"
                    print(msg)
                    
                    # Envoyer l'info au téléphone via Bluetooth
                    ble.send_status(msg)

                    # Logique Autonome Simple
                    if mode_autonome:
                        if objet_detecte['position'] == 'gauche':
                            nav.tourner_angle_gauche(15)
                        elif objet_detecte['position'] == 'droite':
                            nav.tourner_angle_droit(15)
                        elif objet_detecte['position'] == 'centre':
                            # Si c'est au centre, on pourrait avancer un peu
                            # nav.avancer() # Attention c'est bloquant pour l'instant
                            pass

            # Petite pause pour ne pas surcharger le CPU (si la caméra n'a pas son propre waitKey)
            # time.sleep(0.01) 

    except KeyboardInterrupt:
        print("\nArrêt du programme...")
    except Exception as e:
        print(f"\nErreur inattendue : {e}")
    finally:
        # Nettoyage propre des ressources
        print("Nettoyage des ressources...")
        ble.stop()
        nav.cleanup()
        camera.release()
        print("Terminé.")

if __name__ == "__main__":
    main()

