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
    navigation = facade_navigation.FacadeNavigation()
    camera = Camera(model_path="yolov13n.pt")

    try:
        while True:
            objet = camera.detecter_objets(classe_cible="person")
            
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
