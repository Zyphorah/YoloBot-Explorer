import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2
from libcamera import Transform
import os
import matplotlib.pyplot as plt


def gui_available():
    return os.environ.get("DISPLAY") is not None or os.environ.get("WAYLAND_DISPLAY") is not None


class Camera:
    def __init__(self, model_path: str):
        print("Camera: initialisation Picamera2")
        self.use_gui = gui_available()
        print(f"Camera: mode affichage {'GUI' if self.use_gui else 'HEADLESS'}")

        if not self.use_gui:
            os.environ["QT_QPA_PLATFORM"] = "offscreen"
        else:
            if os.environ.get("WAYLAND_DISPLAY"):
                os.environ["QT_QPA_PLATFORM"] = "wayland"
            elif os.environ.get("DISPLAY"):
                os.environ["QT_QPA_PLATFORM"] = "xcb"
            else:
                self.use_gui = False

        try:
            self.picam2 = Picamera2()
            config = self.picam2.create_preview_configuration(
                main={"size": (640, 640)},
                transform=Transform(vflip=True)  
            )
            self.picam2.configure(config)
            self.picam2.start()

            if self.use_gui:
                plt.ion()  # Enable interactive mode for real-time updates
                self.fig, self.ax = plt.subplots()
                self.im = self.ax.imshow(np.zeros((640, 640, 3), dtype=np.uint8))
                plt.title('Detection Camera')

            print("Camera: démarrée avec succès")

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
        
        # Convert frame from BGR to HSV
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Save the captured frame for debugging (convert back to BGR for normal colors)
        cv2.imwrite("debug_captured_frame.jpg", cv2.cvtColor(frame, cv2.COLOR_HSV2BGR))
        results = self.model.predict(frame, verbose=False)[0]
        objet_detecte = None
        
        print(f"Camera: objet détecté '{objet_detecte}'")
        print(f"Résultats: {results}")

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
                    
        if self.use_gui:
            try:
                self.im.set_data(cv2.cvtColor(frame, cv2.COLOR_HSV2RGB))
                plt.draw()
                plt.pause(0.01)  # Small pause for update
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
            plt.close('all')
