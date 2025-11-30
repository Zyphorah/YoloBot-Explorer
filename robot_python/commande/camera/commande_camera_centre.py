from commande.interfaces.i_commande import ICommande


class CommandeCameraCentre(ICommande):
    """Commande pour centrer la caméra."""
    
    def __init__(self, servo):
        self.servo = servo
    
    def executer(self) -> dict:
        self.servo.tourner(90)
        return {}
    
    def get_nom(self) -> str:
        return "cam_centre"
