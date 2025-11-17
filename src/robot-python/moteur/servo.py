from moteur.interfaces.i_cleanup import ICleanup
from moteur.interfaces.i_rotation_angle import IRotation_angle

from Adafruit_PCA9685 import PCA9685
from time import sleep

class Servo(IRotation_angle, ICleanup): 
    def __init__(self):
        self.pwm = PCA9685(busnum=1)
        # Définir les limites de pulse pour 0° et 180°
        self.min_pulse = 150
        self.max_pulse = 600
        self.min_angle = 0
        self.max_angle = 180

    def angle_to_pulse(self, angle):
        angle = max(self.min_angle, min(self.max_angle, angle))
        pulse = int(self.min_pulse + (self.max_pulse - self.min_pulse) * (angle - self.min_angle) / (self.max_angle - self.min_angle))
        return pulse

    def tourner(self, angle):
        self.pwm.set_pwm_freq(60)
        channel = 0
        pulse = self.angle_to_pulse(angle)
        self.pwm.set_pwm(channel, 0, pulse)
        sleep(1)

 
    def cleanup(self):
        self.pwm = None