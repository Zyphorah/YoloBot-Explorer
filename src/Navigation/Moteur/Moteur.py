from Navigation.Moteur.Interfaces.IDirection import IDirection

class Moteur(IDirection):

    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2

    def avancer(self):
        self.n1.on()
        self.n2.off()

    def reculer(self):
        self.n1.off()
        self.n2.on()

    def arreter(self):
        self.n1.off()
        self.n2.off()
    
    def cleanup(self):
        self.n1.close()
        self.n2.close()