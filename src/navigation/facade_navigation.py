from gpiozero import DigitalOutputDevice
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

    def avancer(self):
        self.moteurA.avancer()
        self.moteurB.avancer()

    def reculer(self):
        self.moteurA.reculer()
        self.moteurB.reculer()

    def arreter(self):
        self.moteurA.arreter()
        self.moteurB.arreter()

    def cleanup(self):
        self.moteurA.cleanup()
        self.moteurB.cleanup()

