from time import sleep
import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2
import os


def gui_available():
    return os.environ.get("DISPLAY") is not None or os.environ.get("WAYLAND_DISPLAY") is not None


class Camera:
    def __init__(self, model_path: str):
        print("Camera: initialisation Picamera2")
        self.use_gui = gui_available()
        print(f"Camera: mode affichage {'GUI' if self.use_gui else 'HEADLESS'}")

        if not self.use_gui:
            os.environ["QT_QPA_PLATFORM"] = "offscreen"

        try:
            self.picam2 = Picamera2()
            config = self.picam2.create_preview_configuration(
                main={"size": (640, 480), "format": "BGR888"}
            )
            self.picam2.configure(config)
            self.picam2.start()

            if self.use_gui:
                try:
                    cv2.namedWindow('Detection Camera', cv2.WINDOW_NORMAL)
                except Exception as e:
                    print(f"Camera: impossible d initialiser la fenetre GUI ({e})")
                    self.use_gui = False

            print("Camera: demarree avec succes")

        except Exception as e:
            print(f"Camera: erreur critique lors de l ouverture: {e}")
            self.picam2 = None
            raise e

        self.model = YOLO(model_path)

    def detecter_objets(self, classe_cible: str) -> dict:
        if self.picam2 is None:
            return None

        try:
            frame = self.picam2.capture_array()
            if frame is not None and np.mean(frame) == 0:
                print("Camera: attention image totalement noire")
        except Exception as e:
            print(f"Camera: erreur de capture: {e}")
            return None

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
                        "position": (
                            'centre' if abs(centre_x - largeur_frame / 2) < 50
                            else ('gauche' if centre_x < largeur_frame / 2 else 'droite')
                        )
                    }

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    texte = f"{nom_classe} {confiance:.2f}"
                    cv2.putText(frame, texte, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if self.use_gui:
            try:
                cv2.imshow('Detection Camera', frame)
                cv2.waitKey(1)
            except Exception as e:
                print(f"Camera: erreur affichage GUI: {e}")
                self.use_gui = False

        return objet_detecte

    def release(self):
        print("Camera: liberation ressources")
        if self.picam2:
            self.picam2.stop()
            self.picam2.close()
        if self.use_gui:
            cv2.destroyAllWindows()
