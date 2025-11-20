from time import sleep
import cv2
import numpy as np
from ultralytics import YOLO, YOLOWorld

# Gestion de l'import de Picamera2
try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None
    print("ERREUR: La librairie 'picamera2' n'est pas installée.")

class Camera:
    def __init__(self, model_path: str) :
        if Picamera2 is None:
            raise RuntimeError("Impossible de démarrer : Picamera2 manquant.")

        try:
            print("Initialisation de Picamera2...")
            self.picam2 = Picamera2()
            
            # Configuration : 640x480 en format BGR888 (format natif OpenCV)
            config = self.picam2.create_preview_configuration(main={"size": (640, 480), "format": "BGR888"})
            self.picam2.configure(config)
            self.picam2.start()
            print("Caméra démarrée avec succès.")
        except Exception as e:
            print(f"ERREUR CRITIQUE lors de l'ouverture de la caméra : {e}")
            self.picam2 = None

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
        except cv2.error:
            # Ignore l'erreur si pas d'interface graphique (SSH)
            pass

        return objet_detecte

    def release(self):
        if self.picam2:
            self.picam2.stop()
            self.picam2.close()
        cv2.destroyAllWindows()
