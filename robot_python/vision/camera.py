import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2
from libcamera import Transform
import os
import matplotlib.pyplot as plt


# Définition des plages de couleurs en HSV
# Format: (lower_bound, upper_bound) pour chaque couleur
COLOR_RANGES = {
    "rouge": [
        (np.array([0, 100, 100]), np.array([10, 255, 255])),      # Rouge bas
        (np.array([160, 100, 100]), np.array([180, 255, 255]))    # Rouge haut
    ],
    "red": [
        (np.array([0, 100, 100]), np.array([10, 255, 255])),
        (np.array([160, 100, 100]), np.array([180, 255, 255]))
    ],
    "vert": [(np.array([35, 100, 100]), np.array([85, 255, 255]))],
    "green": [(np.array([35, 100, 100]), np.array([85, 255, 255]))],
    "bleu": [(np.array([100, 100, 100]), np.array([130, 255, 255]))],
    "blue": [(np.array([100, 100, 100]), np.array([130, 255, 255]))],
    "jaune": [(np.array([20, 100, 100]), np.array([35, 255, 255]))],
    "yellow": [(np.array([20, 100, 100]), np.array([35, 255, 255]))],
    "orange": [(np.array([10, 100, 100]), np.array([20, 255, 255]))],
    "violet": [(np.array([130, 100, 100]), np.array([160, 255, 255]))],
    "purple": [(np.array([130, 100, 100]), np.array([160, 255, 255]))],
    "rose": [(np.array([140, 50, 100]), np.array([170, 255, 255]))],
    "pink": [(np.array([140, 50, 100]), np.array([170, 255, 255]))],
    "blanc": [(np.array([0, 0, 200]), np.array([180, 30, 255]))],
    "white": [(np.array([0, 0, 200]), np.array([180, 30, 255]))],
    "noir": [(np.array([0, 0, 0]), np.array([180, 255, 50]))],
    "black": [(np.array([0, 0, 0]), np.array([180, 255, 50]))],
    "cyan": [(np.array([85, 100, 100]), np.array([100, 255, 255]))],
}


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

    def detecter_couleur(self, frame_bgr: np.ndarray, bbox: tuple, couleur_cible: str) -> dict:
        """
        Détecte si la couleur cible est présente dans la région de la bounding box.
        
        Args:
            frame_bgr: Image en format BGR
            bbox: Tuple (x1, y1, x2, y2) de la bounding box
            couleur_cible: Nom de la couleur à détecter
            
        Returns:
            dict avec les infos de couleur ou None si couleur non trouvée
        """
        if couleur_cible is None:
            return {"couleur_detectee": None, "couleur_match": True, "pourcentage": 100}
        
        couleur_cible = couleur_cible.lower().strip()
        
        if couleur_cible not in COLOR_RANGES:
            print(f"Camera: couleur '{couleur_cible}' non reconnue")
            return {"couleur_detectee": "inconnue", "couleur_match": False, "pourcentage": 0}
        
        x1, y1, x2, y2 = bbox
        # Extraire la région d'intérêt (ROI)
        roi = frame_bgr[y1:y2, x1:x2]
        
        if roi.size == 0:
            return {"couleur_detectee": None, "couleur_match": False, "pourcentage": 0}
        
        # Convertir en HSV
        roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Créer le masque pour la couleur cible
        mask = np.zeros(roi_hsv.shape[:2], dtype=np.uint8)
        for lower, upper in COLOR_RANGES[couleur_cible]:
            mask = cv2.bitwise_or(mask, cv2.inRange(roi_hsv, lower, upper))
        
        # Calculer le pourcentage de pixels de la couleur cible
        total_pixels = roi_hsv.shape[0] * roi_hsv.shape[1]
        color_pixels = cv2.countNonZero(mask)
        pourcentage = (color_pixels / total_pixels) * 100 if total_pixels > 0 else 0
        
        # Seuil de 15% pour considérer que la couleur est présente
        couleur_match = pourcentage >= 15
        
        return {
            "couleur_detectee": couleur_cible if couleur_match else self._detecter_couleur_dominante(roi_hsv),
            "couleur_match": couleur_match,
            "pourcentage": round(pourcentage, 1)
        }
    
    def _detecter_couleur_dominante(self, roi_hsv: np.ndarray) -> str:
        """
        Détecte la couleur dominante dans une région HSV.
        """
        best_color = "inconnue"
        best_percentage = 0
        
        for color_name, ranges in COLOR_RANGES.items():
            # Ignorer les doublons (versions françaises/anglaises)
            if color_name in ["red", "green", "blue", "yellow", "purple", "pink", "white", "black"]:
                continue
                
            mask = np.zeros(roi_hsv.shape[:2], dtype=np.uint8)
            for lower, upper in ranges:
                mask = cv2.bitwise_or(mask, cv2.inRange(roi_hsv, lower, upper))
            
            total_pixels = roi_hsv.shape[0] * roi_hsv.shape[1]
            color_pixels = cv2.countNonZero(mask)
            pourcentage = (color_pixels / total_pixels) * 100 if total_pixels > 0 else 0
            
            if pourcentage > best_percentage:
                best_percentage = pourcentage
                best_color = color_name
        
        return best_color if best_percentage >= 10 else "inconnue"

    def detecter_objets(self, classe_cible: str, couleur_cible: str = None) -> dict:
        if self.picam2 is None:
            return None

        try:
            frame = self.picam2.capture_array()
            if frame is not None and np.mean(frame) == 0:
                print("Camera: attention image totalement noire")
        except Exception as e:
            print(f"Camera: erreur de capture: {e}")
            return None
        
        # Convertir RGBA en BGR si nécessaire (Picamera2 peut retourner 4 canaux)
        if frame.shape[2] == 4:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        else:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        
        # Save the captured frame for debugging
        cv2.imwrite("debug_captured_frame.jpg", frame_bgr)
        
        try:
            results = self.model.predict(frame_rgb, verbose=False)[0]
        except Exception as e:
            print(f"Camera: erreur de prediction YOLO: {e}")
            return None
            
        objet_detecte = None

        try:
            boxes = results.boxes
            for box in boxes:
                cls = int(box.cls[0])
                nom_classe = self.model.names[cls]

                if nom_classe == classe_cible:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confiance = float(box.conf[0])
                    centre_x = (x1 + x2) // 2
                    largeur_frame = frame_bgr.shape[1]
                    
                    # Détection de couleur si une couleur cible est spécifiée
                    info_couleur = self.detecter_couleur(frame_bgr, (x1, y1, x2, y2), couleur_cible)
                    
                    # Si une couleur cible est spécifiée mais ne correspond pas, ignorer cet objet
                    if couleur_cible and not info_couleur["couleur_match"]:
                        print(f"Camera: {nom_classe} trouvé mais couleur '{info_couleur['couleur_detectee']}' != '{couleur_cible}'")
                        continue

                    objet_detecte = {
                        "classe": nom_classe,
                        "boite": (x1, y1, x2, y2),
                        "confiance": confiance,
                        "position": (
                            'centre' if abs(centre_x - largeur_frame / 2) < 50
                            else ('gauche' if centre_x < largeur_frame / 2 else 'droite')
                        ),
                        "couleur": info_couleur["couleur_detectee"],
                        "couleur_pourcentage": info_couleur["pourcentage"]
                    }
                    print(f"Camera: {nom_classe} {info_couleur['couleur_detectee']} détecté à {objet_detecte['position']}")
                    break  # Prendre le premier objet correspondant
        except Exception as e:
            print(f"Camera: erreur lors du traitement des résultats: {e}")
            return None
                    
        if self.use_gui:
            try:
                self.im.set_data(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
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
