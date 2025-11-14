from Adafruit_PCA9685 import PCA9685
from time import sleep

pwm = PCA9685(busnum=1)  
pwm.set_pwm_freq(60)

channel = 0
min_pulse = 150
max_pulse = 600

while True:
    pwm.set_pwm(channel, 0, min_pulse)
    sleep(1)
    pwm.set_pwm(channel, 0, max_pulse)
    sleep(1)
