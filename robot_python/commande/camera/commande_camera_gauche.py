from commande.interfaces.i_commande import ICommande


class CommandeCameraGauche(ICommande):
    """Commande pour tourner la caméra à gauche."""
    
    def __init__(self, servo):
        self.servo = servo
    
    def executer(self) -> dict:
        self.servo.tourner(180)
        return {}
    
    def get_nom(self) -> str:
        return "cam_gauche"
