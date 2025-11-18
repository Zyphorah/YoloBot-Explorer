from moteur.servo import Servo
from navigation.facade_navigation import FacadeNavigation
##pybluez

facade_nav = FacadeNavigation()
camera = Servo()

camera.tourner(180)
camera.tourner(90)
camera.tourner(0)

