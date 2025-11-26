from time import sleep
import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2

class Camera:
    def __init__(self, model_path: str) :
        print("Initialisation de Picamera2...")
        try:
            self.picam2 = Picamera2()
            
            # Configuration : 640x480 en format BGR888 (format natif OpenCV)
            # Identique à test_picamera2.py
            config = self.picam2.create_preview_configuration(main={"size": (640, 480), "format": "BGR888"})
            self.picam2.configure(config)
            self.picam2.start()
            
            # Initialisation explicite de la fenêtre pour éviter les erreurs de thread Qt plus tard
            try:
                cv2.namedWindow('Detection Camera', cv2.WINDOW_NORMAL)
            except Exception as e:
                print(f"Attention: Impossible d'initialiser l'interface graphique ({e})")

            print("Caméra démarrée avec succès.")
        except Exception as e:
            print(f"ERREUR CRITIQUE lors de l'ouverture de la caméra : {e}")
            self.picam2 = None
            raise e # On relève l'exception pour ne pas démarrer le robot sans caméra si c'est critique

        self.model = YOLO(model_path)
        # self.model_world = YOLOWorld(model_world)
        # self.model_world.set_classes(["person", "ball"])

    def detecter_objets(self, classe_cible: str) -> dict:
        """Detecte les objets dans le flux vidéo en temps réel."""
        
        if self.picam2 is None:
            return None

        try:
            # Capture d'une frame directement en format compatible OpenCV (numpy array)
            frame = self.picam2.capture_array()
            # DEBUG: Vérifier si l'image est noire
            if frame is not None:
                moyenne = np.mean(frame)
                # print(f"DEBUG: Frame shape={frame.shape}, Mean={moyenne:.2f}")
                if moyenne == 0:
                    print("ATTENTION: L'image capturée est totalement NOIRE.")
        except Exception as e:
            print(f"Erreur de capture : {e}")
            return None
        
        # Le reste du traitement est identique car 'frame' est une image OpenCV standard
        results = self.model(frame, verbose=False)[0]
        objet_detecte = None

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                nom_classe = self.model.names[cls]

                if nom_classe == classe_cible:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confiance = float(box.conf[0])
                    centre_x = (x1 + x2) // 2
                    largeur_frame = frame.shape[1]
                    objet_detecte = {
                        "classe": nom_classe,
                        "boite": (x1, y1, x2, y2),
                        "confiance": confiance,
                        "position": 'centre' if abs(centre_x - largeur_frame/2) < 50 
                                   else ('gauche' if centre_x < largeur_frame/2 else 'droite')
                    }
                    
                    # Dessiner le rectangle et le texte sur la frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    texte = f"{nom_classe} {confiance:.2f}"
                    cv2.putText(frame, texte, (x1, y1 - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Afficher la frame avec les détections
        try:
            cv2.imshow('Detection Camera', frame)
            cv2.waitKey(1)
        except Exception as e:
            # On attrape tout pour éviter que le robot ne crash à cause de l'affichage
            # (Erreurs Qt, thread, ou absence d'écran)
            print(f"Erreur affichage: {e}")

        return objet_detecte

    def release(self):
        if self.picam2:
            self.picam2.stop()
            self.picam2.close()
        cv2.destroyAllWindows()
