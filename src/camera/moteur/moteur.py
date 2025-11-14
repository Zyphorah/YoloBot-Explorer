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
        self._mock = False  # fallback flag

        try:
            # Attempt normal hardware initialization (may raise PermissionError if /dev/i2c-1 is not accessible)
            import busio
            from board import SCL, SDA
            # This line is the one that raised PermissionError in your trace:
            i2c = busio.I2C(SCL, SDA)

            # PCA9685 setup (keep your existing initialization here)
            from adafruit_pca9685 import PCA9685
            self._pca = PCA9685(i2c)
            self._pca.frequency = freq

            self.channel = channel
            self.angle_min = angle_min
            self.angle_max = angle_max
            self.angle_neutre = angle_neutre
            self.pulse_min_us = pulse_min_us
            self.pulse_max_us = pulse_max_us
            self.freq = freq

            # Place la caméra en position neutre au démarrage
            self._set_angle(self.angle_neutre)
        except (PermissionError, OSError) as e:
            # Common on non-root or CI/desktop environments where /dev/i2c-1 is inaccessible.
            print(
                "Warning: I2C initialization failed (no access to /dev/i2c-1). "
                "Falling back to mock motor mode. To use real hardware, run as root or add your user to the i2c group "
                "and enable I2C (and ensure /dev/i2c-1 exists)."
            )
            self._mock = True
            # Minimal mock internal state so methods can run without hardware
            self._angle = angle_neutre
            self._channel = channel
            self._angle_min = angle_min
            self._angle_max = angle_max
            self._angle_neutre = angle_neutre
        except Exception as e:
            # Any other initialization failure: log and fallback to mock
            print(f"Warning: PCA9685/I2C init failed ({e}). Falling back to mock motor mode.")
            self._mock = True
            self._angle = angle_neutre
            self._channel = channel
            self._angle_min = angle_min
            self._angle_max = angle_max
            self._angle_neutre = angle_neutre

    # === API Direction ===

    def tourner_gauche(self):
        """Tourne la caméra vers la gauche (angle_min)."""
        if getattr(self, "_mock", False):
            # Simulate motion without hardware
            self._angle = max(self._angle_min, getattr(self, "_angle", self._angle_neutre) - 10)
            print(f"MOCK: tourner_gauche() -> angle={self._angle}")
            return
        self._set_angle(self.angle_min)

    def tourner_droite(self):
        """Tourne la caméra vers la droite (angle_max)."""
        if getattr(self, "_mock", False):
            self._angle = min(self._angle_max, getattr(self, "_angle", self._angle_neutre) + 10)
            print(f"MOCK: tourner_droite() -> angle={self._angle}")
            return
        self._set_angle(self.angle_max)

    def arreter(self):
        """Reviens à la position neutre (centre)."""
        if getattr(self, "_mock", False):
            print("MOCK: arreter()")
            return
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
        if getattr(self, "_mock", False):
            # Nothing to cleanup in mock mode
            print("MOCK: cleanup()")
            return
        self.pca.channels[self.channel].duty_cycle = 0
        self.pca.deinit()
