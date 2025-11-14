from time import sleep
import cv2
from ultralytics import YOLO, YOLOWorld


class Camera:
    def __init__(self, model_path: str) :
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO(model_path)
        # self.model_world = YOLOWorld(model_world)

        # self.model_world.set_classes(["person", "ball"])

    def detecter_objets(self, classe_cible: str) -> dict:
        """Detecte les objets dans le flux vidéo en temps réel."""
        sleep(0.32)
        ret, frame = self.cap.read()
        
        if not ret:
            return None
        print("Frame : ", frame.shape)
        results = self.model(frame)[0]
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
        cv2.imshow('Detection Camera', frame)
        cv2.waitKey(1)  # Nécessaire pour rafraîchir la fenêtre

        return objet_detecte

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
