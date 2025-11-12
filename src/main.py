import time
from navigation import facade_navigation

navigation = facade_navigation.FacadeNavigation()

while True:
    collision = navigation.avancer()
    if collision:
        print("Collision! Je recule...")
        navigation.reculer()
        time.sleep(1)
        navigation.arreter()
        print("Je tourne...")
        navigation.tourner_angle_droit(angle=90, duree=1)
