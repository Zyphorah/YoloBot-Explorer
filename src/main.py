# import time
# from navigation import facade_navigation

# navigation = facade_navigation.FacadeNavigation()

# while True:
#     collision = navigation.avancer()
#     if collision:
#         print("Collision! Je recule...")
#         navigation.reculer()
#         time.sleep(1)
#         navigation.arreter()
#         print("Je tourne...")
#         navigation.tourner_angle(angle=90, duree=1)

import time
from navigation import facade_navigation
from vision.camera import Camera


def main():
    ##navigation = facade_navigation.FacadeNavigation()
    # Prefer local custom weights if present, otherwise try a known fallback
    requested_weights = "yolov8n.pt"
    fallback_weights = "yolov8n.pt"

    model_to_use = requested_weights if os.path.exists(requested_weights) else fallback_weights

    try:
        camera = Camera(model_path=model_to_use)
    except FileNotFoundError as e:
        print(f"Poids introuvables: '{requested_weights}' et le fallback '{fallback_weights}' n'a pas pu être chargé.")
        print("Placez le fichier de poids dans le répertoire courant ou modifiez `requested_weights` dans main.py.")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la caméra/modèle: {e}")
        print("Vérifiez que la dépendance 'ultralytics' et 'torch' sont installées et configurées.")
        sys.exit(1)

    try:
        while True:
            objet = camera.detecter_objets(classe_cible="animal")

            if objet:
                print(f"Objets detectes: {objet} à la position {objet['position']}")

                if objet['position'] == 'centre':
                    collision = navigation.avancer()
                    if collision:
                        print("Collision! Je recule...")
                        navigation.reculer()
                        time.sleep(1)
                        navigation.arreter()
                        print("Je tourne...")
                        navigation.tourner_angle_droit(angle=90)
                elif objet['position'] == 'gauche':
                    print("Objet a gauche, je tourne a droite.")
                    navigation.tourner_angle_droit(angle=45)
                elif objet['position'] == 'droite':
                    print("Objet a droite, je tourne a gauche.")
                    navigation.tourner_angle_droit(angle=-45)
            else:
                print("Aucun objet detecte, je cherche...")
                navigation.tourner_angle_droit(angle=30)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Arret du programme.")
    finally:
        navigation.arreter()
        camera.release()
main()
