import time
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

def test_picamera_legacy():
    print("--- Démarrage du test Picamera (Legacy) ---")

    try:
        # Initialisation de la caméra
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        
        # Attendre que la caméra chauffe
        time.sleep(2)
        
        # Initialisation du buffer pour OpenCV
        # PiRGBArray permet de convertir directement le flux en format compatible OpenCV
        rawCapture = PiRGBArray(camera, size=(640, 480))
        
        print("Caméra démarrée avec succès (Picamera Legacy) !")
        print("Appuyez sur 'q' pour quitter.")

        frame_count = 0
        
        # Capture continue du flux
        # use_video_port=True est important pour la vitesse
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # Récupération de l'image sous forme de tableau numpy
            image = frame.array
            frame_count += 1
            
            # --- Traitement OpenCV ici ---
            cv2.putText(image, f"Picamera Legacy - Frame {frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # --- Affichage ---
            try:
                cv2.imshow("Test Picamera Legacy", image)
                key = cv2.waitKey(1) & 0xFF
                
                # IMPORTANT : Il faut vider le buffer avant la prochaine frame
                rawCapture.truncate(0)
                
                if key == ord("q"):
                    break
            except cv2.error:
                # Si pas d'écran (SSH), on vide quand même le buffer
                rawCapture.truncate(0)
                if frame_count % 30 == 0:
                    print(f"Flux actif... Frame {frame_count}")

    except Exception as e:
        print(f"\nERREUR : {e}")
        print("Assurez-vous que le mode 'Legacy Camera' est ACTIVÉ dans raspi-config.")
        print("Si vous êtes sur Bullseye/Bookworm, essayez plutôt Picamera2 ou libcamera.")

    finally:
        try:
            camera.close()
        except:
            pass
        cv2.destroyAllWindows()
        print("Caméra arrêtée.")

