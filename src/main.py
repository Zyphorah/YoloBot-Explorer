from gpiozero import DigitalOutputDevice
from navigation.moteur.moteur import Moteur
import time

# GPIO pins en mode BCM (converti de BOARD)
# N1 sur la pin 15 (BOARD) = GPIO 22 (BCM)
# N2 sur la pin 13 (BOARD) = GPIO 27 (BCM)
# N3 sur la pin 7 (BOARD) = GPIO 4 (BCM)
# N4 sur la pin 11 (BOARD) = GPIO 17 (BCM)

N1 = DigitalOutputDevice(22)
N2 = DigitalOutputDevice(27)
N3 = DigitalOutputDevice(4)
N4 = DigitalOutputDevice(17)

moteurA = Moteur(N1, N2)
moteurB = Moteur(N3, N4)

try:
     for i in range(3):
       moteurA.avancer()
       moteurB.avancer()
       time.sleep(1)
       moteurA.reculer()
       moteurB.reculer()
       time.sleep(1)
finally: 
    moteurA.cleanup()
    moteurB.cleanup()
