import cv2
import time
import sys

def test_camera():
    print("--- Démarrage du test caméra ---")
    
    # 1. Tentative d'ouverture avec V4L2 (Recommandé pour Raspberry Pi)
    print("Tentative d'ouverture avec le backend V4L2...")
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    
    # 2. Si échec, tentative standard
    if not cap.isOpened():
        print("Échec V4L2. Tentative avec le backend par défaut...")
        cap = cv2.VideoCapture(0)
        
    # 3. Vérification finale
    if not cap.isOpened():
        print("\nERREUR CRITIQUE : Impossible d'ouvrir la caméra.")
        print("Vérifiez :")
        print(" - Que la caméra est branchée.")
        print(" - Vos permissions (sudo usermod -a -G video $USER).")
        print(" - Si 'libcamera' ne bloque pas l'accès (essayez 'sudo raspi-config' -> Interface -> Legacy Camera).")
        return

    # Récupération des infos
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    backend = cap.getBackendName()
    
    print(f"\nCaméra ouverte avec succès !")
    print(f"Backend utilisé : {backend}")
    print(f"Résolution : {int(width)}x{int(height)}")
    print(f"FPS théorique : {fps}")
    print("\nAppuyez sur 'q' dans la fenêtre ou 'Ctrl+C' dans le terminal pour quitter.\n")

    frame_count = 0
    start_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Erreur : Impossible de lire une image (frame vide).")
                time.sleep(1)
                continue

            frame_count += 1
            
            # Ajout d'un texte sur l'image pour prouver que le traitement fonctionne
            cv2.putText(frame, f"Test OK - Frame {frame_count}", (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Tentative d'affichage (peut échouer en SSH sans X11)
            try:
                cv2.imshow('Test Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Sortie demandée par l'utilisateur.")
                    break
            except cv2.error:
                # Mode sans tête (Headless) : on affiche juste un log
                if frame_count % 30 == 0:
                    print(f"Flux vidéo actif... Frame {frame_count} capturée.")

    except KeyboardInterrupt:
        print("\nArrêt du script.")
    
    finally:
        # Nettoyage propre
        cap.release()
        cv2.destroyAllWindows()
        print("Caméra libérée et fenêtres fermées.")

if __name__ == "__main__":
    test_camera()
    