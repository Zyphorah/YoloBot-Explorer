import os
import time
import threading

# Imports des modules du projet
from services.ble_service import BLEService
from navigation.facade_navigation import FacadeNavigation
from moteur.servo import Servo
from vision.camera import Camera

def demarrer_ble(ble_service):
    ble_service.start()
    print("Service BLE démarré (thread séparé).")

def main():
    print("--- Initialisation du Robot ---")

    # 1. Initialisation de la Caméra (Doit être fait AVANT le BLE pour éviter les conflits de thread Qt/GLib)
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

    # 2. Initialisation du Bluetooth
    ble = BLEService()
    ble.start()
    print("Service BLE démarré.")

    # 3. Initialisation de la Navigation et du Servo
    nav = FacadeNavigation()

    servo_camera = Servo()
    servo_camera.tourner(90) # Position centrale par défaut

    print("--- Robot Prêt ---")
    print("En attente de commandes BLE ou de détection...")

    # Variables d'état
    mode_detection = True
    mode_autonome = True
    action_courante = "stop" # Pour savoir si on recule ou avance
    debut_rotation = 0 # Timestamp pour gérer la durée de rotation
    objet_cible = "person" # Objet à détecter par défaut

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
                    action_courante = "avancer"
                elif "reculer" in commande:
                    nav.reculer()
                    action_courante = "reculer"
                elif "gauche" in commande:
                    nav.tourner_gauche()
                    action_courante = "tourner_gauche_90"
                    debut_rotation = time.time()
                elif "droite" in commande:
                    nav.tourner_droite()
                    action_courante = "tourner_droite_90"
                    debut_rotation = time.time()
                elif "stop" in commande:
                    nav.arreter()
                    action_courante = "stop"
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
                
                # Commandes Configuration
                elif "set_object" in commande:
                    # Format attendu: set_object:person
                    try:
                        _, new_target = commande.split(":")
                        objet_cible = new_target.strip()
                        print(f"Nouvelle cible de détection : {objet_cible}")
                    except ValueError:
                        print("Erreur format set_object. Attendu: set_object:classe")

            # --- B. GESTION CAMÉRA ---
            if mode_detection or mode_autonome:
                # On cherche l'objet cible
                objet_detecte = camera.detecter_objets(objet_cible)
                print(objet_detecte)

                if objet_detecte:
                    msg = f"Vu: {objet_detecte['classe']} ({objet_detecte['position']})"
                    print(msg)
                    
                    # Envoyer l'info au téléphone via Bluetooth
                    ble.send_status(msg)

                    # Logique Autonome Simple
                    if mode_autonome:
                        if objet_detecte['position'] == 'gauche':
                            nav.tourner_angle_gauche(15)
                            if action_courante == "avancer":
                                nav.avancer()
                        elif objet_detecte['position'] == 'droite':
                            nav.tourner_angle_droit(15)
                            if action_courante == "avancer":
                                nav.avancer()
                        elif objet_detecte['position'] == 'centre':
                            # Si c'est au centre, on pourrait avancer un peu
                            # nav.avancer() # Attention c'est bloquant pour l'instant
                            pass
            
            # --- C. GESTION ROTATION AUTOMATIQUE ---
            if action_courante in ["tourner_gauche_90", "tourner_droite_90"]:
                if time.time() - debut_rotation >= 1.0:
                    print("Fin de rotation 90°, passage en mode AVANCER")
                    nav.avancer()
                    action_courante = "avancer"

            # --- D. GESTION COLLISION ---
            # On vérifie la collision à chaque tour de boucle pour arrêter le robot si nécessaire
            # On ne vérifie PAS la collision si on recule (pour pouvoir se dégager d'un obstacle)
            if action_courante != "reculer":
                if nav.verifier_collision():
                    action_courante = "stop"

            # Petite pause pour ne pas surcharger le CPU (si la caméra n'a pas son propre waitKey)
            # time.sleep(0.01) 

    except KeyboardInterrupt:
        print("\nArrêt du programme...")
    except Exception as e:
        print(f"\nErreur inattendue : {e}")
    finally:
        # Nettoyage propre des ressources
        print("Nettoyage des ressources...")
        if 'ble' in locals():
            ble.stop()
        if 'nav' in locals():
            nav.cleanup()
        if 'camera' in locals():
            try:
                camera.release()
            except Exception:
                # Ignorer les erreurs OpenCV (ex: environnement headless sans GUI)
                pass
        print("Terminé.")

if __name__ == "__main__":
    main()

