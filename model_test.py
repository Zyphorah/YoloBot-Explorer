import cv2
import numpy as np
from ultralytics import YOLO

# Définition des plages de couleurs en HSV
COLOR_RANGES = {
    "rouge": [
        (np.array([0, 100, 100]), np.array([10, 255, 255])),
        (np.array([160, 100, 100]), np.array([180, 255, 255]))
    ],
    "vert": [(np.array([35, 100, 100]), np.array([85, 255, 255]))],
    "bleu": [(np.array([100, 100, 100]), np.array([130, 255, 255]))],
    "jaune": [(np.array([20, 100, 100]), np.array([35, 255, 255]))],
    "orange": [(np.array([10, 100, 100]), np.array([20, 255, 255]))],
    "violet": [(np.array([130, 100, 100]), np.array([160, 255, 255]))],
    "blanc": [(np.array([0, 0, 200]), np.array([180, 30, 255]))],
    "noir": [(np.array([0, 0, 0]), np.array([180, 255, 50]))],
}


def detect_color(image_bgr, bbox):
    """Détecte la couleur dominante dans une bounding box."""
    x1, y1, x2, y2 = map(int, bbox)
    roi = image_bgr[y1:y2, x1:x2]
    
    if roi.size == 0:
        return "inconnue", 0
    
    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    best_color = "inconnue"
    best_percentage = 0
    
    for color_name, ranges in COLOR_RANGES.items():
        mask = np.zeros(roi_hsv.shape[:2], dtype=np.uint8)
        for lower, upper in ranges:
            mask = cv2.bitwise_or(mask, cv2.inRange(roi_hsv, lower, upper))
        
        total_pixels = roi_hsv.shape[0] * roi_hsv.shape[1]
        color_pixels = cv2.countNonZero(mask)
        percentage = (color_pixels / total_pixels) * 100 if total_pixels > 0 else 0
        
        if percentage > best_percentage:
            best_percentage = percentage
            best_color = color_name
    
    return best_color, round(best_percentage, 1)


def predict_with_color(image_path, target_shape=None, target_color=None):
    """Prédit les objets et leurs couleurs."""
    model = YOLO("best.pt")
    
    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Erreur: impossible de charger {image_path}")
        return
    
    # Prédiction
    results = model.predict(image, conf=0.20, verbose=False)[0]
    
    print(f"\n=== Résultats pour {image_path} ===")
    print(f"Cible: forme={target_shape or 'toutes'}, couleur={target_color or 'toutes'}")
    print("-" * 50)
    
    for box in results.boxes:
        cls = int(box.cls[0])
        nom_classe = model.names[cls]
        confiance = float(box.conf[0])
        bbox = box.xyxy[0].cpu().numpy()
        
        # Détecter la couleur
        couleur, pourcentage = detect_color(image, bbox)
        
        # Filtrer par cible si spécifié
        if target_shape and nom_classe != target_shape:
            continue
        if target_color and couleur != target_color.lower():
            print(f"  [Ignoré] {nom_classe} ({couleur}) - couleur ne correspond pas à '{target_color}'")
            continue
        
        print(f"  ✓ {nom_classe} ({confiance:.1%}) - Couleur: {couleur} ({pourcentage}%)")
        
        # Dessiner sur l'image
        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{nom_classe} - {couleur}"
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Sauvegarder le résultat
    output_path = f"result_{image_path}"
    cv2.imwrite(output_path, image)
    print(f"\nRésultat sauvegardé: {output_path}")


if __name__ == "__main__":
    # Test basique - détecter tout
    predict_with_color("img1.jpeg")
    
    # Exemple: détecter seulement les objets rouges
    # predict_with_color("img1.jpeg", target_color="rouge")
    
    # Exemple: détecter seulement les personnes en bleu
    # predict_with_color("img1.jpeg", target_shape="person", target_color="bleu")