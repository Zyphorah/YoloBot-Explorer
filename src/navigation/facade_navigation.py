from gpiozero import DigitalOutputDevice, DistanceSensor
from navigation.gestion_collision.collision import collision
from navigation.gestion_collision.radar import Radar
from navigation.moteur.moteur import Moteur

class FacadeNavigation:

    def __init__(self):
        # GPIO pins en mode BCM (converti de BOARD)
        # N1 sur la pin 15 (BOARD) = GPIO 22 (BCM)
        # N2 sur la pin 13 (BOARD) = GPIO 27 (BCM)
        # N3 sur la pin 7 (BOARD) = GPIO 4 (BCM)
        # N4 sur la pin 11 (BOARD) = GPIO 17 (BCM)
        self.N1 = DigitalOutputDevice(22)
        self.N2 = DigitalOutputDevice(27)
        self.N3 = DigitalOutputDevice(4)
        self.N4 = DigitalOutputDevice(17)

        self.moteurA = Moteur(self.N1, self.N2)
        self.moteurB = Moteur(self.N3, self.N4)
        
        #HC-SR04 radar
        #VCC → 5V (phys. pin 2 ou 4)
        #GND → GND (phys. pin 6)
        #TRIG → GPIO23 (BCM 23, phys. pin 16)
        #ECHO → GPIO24 (BCM 24, phys. pin 18)
        # TRIG = GPIO23, ECHO = GPIO24

        
        self.radar = Radar(DistanceSensor(echo=24, trigger=23))
        self.collision = collision(self.radar)

    def avancer(self):
        import time
        self.moteurA.avancer()
        self.moteurB.avancer()
        try:
            while True:
                if self.collision.detecter_collision():
                    self.moteurA.arreter()
                    self.moteurB.arreter()
                    print("Collision détectée ! Moteurs arrêtés.")
                    break
                time.sleep(0.1)  # vérifie toutes les 100 ms
        except KeyboardInterrupt:
            self.moteurA.arreter()
            self.moteurB.arreter()

    def reculer(self):
        self.moteurA.reculer()
        self.moteurB.reculer()

    def arreter(self):
        self.moteurA.arreter()
        self.moteurB.arreter()

    def cleanup(self):
        self.moteurA.cleanup()
        self.moteurB.cleanup()

