from camera.moteur.direction import Direction

try:
    # Bibliothèque standard pour PCA9685 (Adafruit)
    from adafruit_pca9685 import PCA9685
    from board import SCL, SDA
    import busio
except ImportError:
    PCA9685 = None  # Permet de tester sans le matériel


class Moteur(Direction):
    """
    Contrôle d'un MicroServo 9g MS18 via un PCA9685 16-channel 12-bit PWM.

    Cette classe est pensée pour orienter la caméra : gauche/droite/arrêt (position neutre).
    """

    def __init__(
        self,
        channel: int = 0,
        freq: int = 50,
        angle_min: float = 0.0,
        angle_max: float = 180.0,
        angle_neutre: float = 90.0,
        pulse_min_us: float = 500.0,
        pulse_max_us: float = 2500.0,
    ):
        if PCA9685 is None:
            raise RuntimeError(
                "La bibliothèque adafruit_pca9685 n'est pas installée. "
                "Installe-la avec 'uv pip install adafruit-circuitpython-pca9685'."
            )

        # Bus I2C
        i2c = busio.I2C(SCL, SDA)
        self.pca = PCA9685(i2c)
        self.pca.frequency = freq

        self.channel = channel
        self.angle_min = angle_min
        self.angle_max = angle_max
        self.angle_neutre = angle_neutre
        self.pulse_min_us = pulse_min_us
        self.pulse_max_us = pulse_max_us
        self.freq = freq

        # Place la caméra en position neutre au démarrage
        self._set_angle(self.angle_neutre)

    # === API Direction ===

    def tourner_gauche(self):
        """Tourne la caméra vers la gauche (angle_min)."""
        self._set_angle(self.angle_min)

    def tourner_droite(self):
        """Tourne la caméra vers la droite (angle_max)."""
        self._set_angle(self.angle_max)

    def arreter(self):
        """Reviens à la position neutre (centre)."""
        self._set_angle(self.angle_neutre)

    # === Internes ===

    def _set_angle(self, angle: float):
        angle = max(self.angle_min, min(self.angle_max, angle))
        pulse_us = self._angle_to_pulse_us(angle)
        duty = self._pulse_us_to_12bit(pulse_us)
        self.pca.channels[self.channel].duty_cycle = duty

    def _angle_to_pulse_us(self, angle: float) -> float:
        """Mappe un angle [angle_min, angle_max] vers une impulsion en µs."""
        span_angle = self.angle_max - self.angle_min
        if span_angle <= 0:
            return (self.pulse_min_us + self.pulse_max_us) / 2.0
        ratio = (angle - self.angle_min) / span_angle
        return self.pulse_min_us + ratio * (self.pulse_max_us - self.pulse_min_us)

    def _pulse_us_to_12bit(self, pulse_us: float) -> int:
        """
        Convertit une durée d'impulsion (µs) en valeur 12 bits (0–65535)
        pour le PCA9685 (duty_cycle).
        """
        period_s = 1.0 / float(self.freq)
        period_us = period_s * 1_000_000.0
        duty_ratio = pulse_us / period_us
        duty_ratio = max(0.0, min(1.0, duty_ratio))
        return int(duty_ratio * 0xFFFF)

    def cleanup(self):
        """Optionnel : désactive le canal."""
        self.pca.channels[self.channel].duty_cycle = 0
        self.pca.deinit()
