from moteur.interfaces.i_cleanup import ICleanup
from moteur.interfaces.i_rotation_angle import IRotation_angle

from Adafruit_PCA9685 import PCA9685
from time import sleep

class Servo(IRotation_angle, ICleanup): 
    CHANNEL = 0
    
    def __init__(self):
        self.pwm = PCA9685(busnum=1)
        self.pwm.set_pwm_freq(60)
        self.min_pulse = 150
        self.max_pulse = 600
        self.min_angle = 0
        self.max_angle = 180
        self._angle_actuel = 90

    def angle_to_pulse(self, angle):
        angle = max(self.min_angle, min(self.max_angle, angle))
        pulse = int(self.min_pulse + (self.max_pulse - self.min_pulse) * (angle - self.min_angle) / (self.max_angle - self.min_angle))
        return pulse

    def tourner(self, angle):
        pulse = self.angle_to_pulse(angle)
        self.pwm.set_pwm(self.CHANNEL, 0, pulse)
        print(f"Servo: tourner a {angle} degres")
        self._angle_actuel = angle
        sleep(0.5)
        self.desactiver()

    def desactiver(self):
        #Désactive le signal PWM pour éviter les mouvements parasites
        self.pwm.set_pwm(self.CHANNEL, 0, 0)

    def cleanup(self):
        self.desactiver()
        self.pwm = None