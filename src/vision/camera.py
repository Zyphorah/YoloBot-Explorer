import cv2
from ultralytics import YOLO


class Camera:
    def __init__(self, model_path: str) :
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO(model_path)

    def detecter_objets(self, classe_cible: str) -> dict:
        """Detecte les objets dans le flux vidéo en temps réel."""
        ret, frame = self.cap.read()
        if not ret:
            return None
        
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

        return objet_detecte

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
