import time
import cv2
import numpy as np
from picamera2 import Picamera2

def test_picamera2():
    print("--- Démarrage du test Picamera2 ---")

    try:
        # Initialisation de Picamera2
        picam2 = Picamera2()
        
        # Configuration de la caméra (résolution, format)
        config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "BGR888"})
        picam2.configure(config)
        
        # Démarrage de la caméra
        picam2.start()
        print("Caméra démarrée avec succès (Picamera2) !")
        print("Appuyez sur 'Ctrl+C' pour quitter.")

        frame_count = 0
        
        while True:
            # Capture d'une image sous forme de tableau numpy (compatible OpenCV)
            # capture_array attend que la frame soit prête
            frame = picam2.capture_array()

            frame_count += 1
            
            # --- Traitement OpenCV ici ---
            cv2.putText(frame, f"Picamera2 - Frame {frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # --- Affichage ---
            try:
                cv2.imshow("Test Picamera2", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except cv2.error:
                # Si pas d'écran (SSH), on affiche juste un log
                if frame_count % 30 == 0:
                    print(f"Flux actif... Frame {frame_count}")

    except Exception as e:
        print(f"\nERREUR : {e}")
        print("Assurez-vous que 'libcamera' est activé et que vous n'utilisez pas le mode 'Legacy Camera'.")

    finally:
        # Nettoyage
        try:
            picam2.stop()
            picam2.close()
        except:
            pass
        cv2.destroyAllWindows()
        print("Caméra arrêtée.")

if __name__ == "__main__":
    test_picamera2()