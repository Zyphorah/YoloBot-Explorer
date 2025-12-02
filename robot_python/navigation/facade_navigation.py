from gpiozero import DigitalOutputDevice, DistanceSensor
import time
from navigation.gestion_collision.anti_collision import Anti_collision
from navigation.gestion_collision.radar import Radar
from moteur.dc import Dc

class FacadeNavigation:

    def tourner_angle_droit(self, angle=90):
        duree = (angle / 90.0) * 1.0
        
        self.moteurA.tourner_gauche() 
        self.moteurB.tourner_droite()  
        time.sleep(duree)
        self.arreter()
    
    def tourner_angle_gauche(self, angle=90):
        duree = (angle / 90.0) * 1.0
        
        self.moteurA.tourner_droite()  
        self.moteurB.tourner_gauche()  
        time.sleep(duree)
        self.arreter()

    def tourner_droite(self):
        self.moteurA.tourner_gauche()
        self.moteurB.tourner_droite()

    def tourner_gauche(self):
        self.moteurA.tourner_droite()
        self.moteurB.tourner_gauche()

    def __init__(self):
        # GPIO pins en mode BCM (converti de BOARD)
        # N1 sur la pin 15 (BOARD) = GPIO 22 (BCM)
        # N2 sur la pin 13 (BOARD) = GPIO 27 (BCM)
        # N3 sur la pin 7 (BOARD) = GPIO 4 (BCM)
        # N4 sur la pin 11 (BOARD) = GPIO 17 (BCM)
        self.N1 = DigitalOutputDevice(22)
        self.N2 = DigitalOutputDevice(27)
        self.N3 = DigitalOutputDevice(6)
        self.N4 = DigitalOutputDevice(17)

        self.moteurA = Dc(self.N1, self.N2)
        self.moteurB = Dc(self.N3, self.N4)
        
        #HC-SR04 radar
        #VCC → 5V (phys. pin 2 ou 4)
        #GND → GND (phys. pin 6)
        #TRIG → GPIO23 (BCM 23, phys. pin 16)
        #ECHO → GPIO24 (BCM 24, phys. pin 18)
        # TRIG = GPIO23, ECHO = GPIO24
        
        self.radar = Radar(DistanceSensor(echo=24, trigger=23))
        self.collision = Anti_collision(self.radar)

    def avancer(self):
        self.moteurA.tourner_droite()
        self.moteurB.tourner_droite()

    def verifier_collision(self):
        if self.collision.detecter_collision():
            self.moteurA.arreter()
            self.moteurB.arreter()
            print("Navigation: collision detectee, moteurs arretes")
            return True
        return False

    def reculer(self):
        self.moteurA.tourner_gauche()
        self.moteurB.tourner_gauche()

    def arreter(self):
        self.moteurA.arreter()
        self.moteurB.arreter()

    def cleanup(self):
        self.moteurA.cleanup()
        self.moteurB.cleanup()
