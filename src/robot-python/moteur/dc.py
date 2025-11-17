from .interfaces.i_rotation import IRotation
from .interfaces.i_cleanup import ICleanup

class Dc(IRotation ,ICleanup):

    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2

    def tourner_droite(self):
        self.n1.off()
        self.n2.on()

    def tourner_gauche(self):
        self.n1.on()
        self.n2.off()

    def arreter(self):
        self.n1.off()
        self.n2.off()
    
    def cleanup(self):
        self.n1.close()
        self.n2.close()
