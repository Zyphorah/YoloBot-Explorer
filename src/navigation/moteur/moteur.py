from   navigation.moteur.interfaces.i_direction import i_direction

class Moteur(i_direction):

    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2

    def avancer(self):
        self.n1.off()
        self.n2.on()

    def reculer(self):
        self.n1.on()
        self.n2.off()

    def arreter(self):
        self.n1.off()
        self.n2.off()
    
    def cleanup(self):
        self.n1.close()
        self.n2.close()
