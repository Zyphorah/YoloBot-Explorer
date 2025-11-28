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

    model_path = "../yolov8n.pt"
    if not os.path.exists(model_path):
        model_path = "yolov8n.pt"
    
    print(f"Chargement du modèle IA depuis {model_path}...")
    try:
        camera = Camera(model_path)
    except Exception as e:
        print(f"Erreur caméra: {e}")
        return

    ble = BLEService()
    ble.start()
    print("Service BLE démarré.")

    nav = FacadeNavigation()

    servo_camera = Servo()
    servo_camera.tourner(90) 

    print("--- Robot Prêt ---")
    print("En attente de commandes BLE ou de détection...")

    mode_detection = True
    mode_autonome = True
    action_courante = "stop" 
    debut_rotation = 0 
    objet_cible = "person" 

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
                try:
                    # On cherche l'objet cible
                    objet_detecte = camera.detecter_objets(objet_cible)
                    # print(objet_detecte) # Trop verbeux si None

                    if objet_detecte:
                        msg = f"Vu: {objet_detecte['classe']} ({objet_detecte['position']})"
                        print(msg)
                        
                        ble.send_status(msg)

                        if mode_autonome:
                            y1, y2 = objet_detecte['boite'][1], objet_detecte['boite'][3]
                            hauteur_objet = y2 - y1
                            hauteur_frame = 480
                            
                            SEUIL_PROXIMITE = 0.40 
                            ratio_hauteur = hauteur_objet / hauteur_frame

                            position = objet_detecte['position']

                            if ratio_hauteur > SEUIL_PROXIMITE:
                                if action_courante != "stop":
                                    nav.arreter()
                                    action_courante = "stop"
                                    print(f"Cible trop proche ({ratio_hauteur:.2f}), arrêt.")
                            
                            elif position == 'gauche':
                                if action_courante != "tourner_gauche":
                                    nav.tourner_gauche()
                                    action_courante = "tourner_gauche"
                                    print("Cible à gauche -> Rotation Gauche")

                            elif position == 'droite':
                                if action_courante != "tourner_droite":
                                    nav.tourner_droite()
                                    action_courante = "tourner_droite"
                                    print("Cible à droite -> Rotation Droite")

                            elif position == 'centre':
                                if action_courante != "avancer":
                                    nav.avancer()
                                    action_courante = "avancer"
                                    print("Cible centrée -> Avancer")
                    else:
                        if mode_autonome and action_courante != "stop":
                            nav.arreter()
                            action_courante = "stop"
                            print("Cible perdue -> Arrêt")
                
                except Exception as e:
                    print(f"ERREUR dans la boucle autonome/caméra : {e}")
                    import traceback
                    traceback.print_exc()
                    nav.arreter()
                    action_courante = "stop"
            
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
        print("Nettoyage des ressources...")
        if 'ble' in locals():
            ble.stop()
        if 'nav' in locals():
            nav.cleanup()
        if 'camera' in locals():
            try:
                camera.release()
            except Exception:
                pass
        print("Terminé.")

if __name__ == "__main__":
    main()

