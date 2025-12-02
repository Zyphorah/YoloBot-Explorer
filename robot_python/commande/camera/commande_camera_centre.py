from commande.interfaces.i_commande import ICommande

class CommandeCameraCentre(ICommande):
    
    def __init__(self, servo):
        self.servo = servo
    
    def executer(self) -> dict:
        self.servo.tourner(90)
        return {}
