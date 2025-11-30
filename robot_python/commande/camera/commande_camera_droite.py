from commande.interfaces.i_commande import ICommande


class CommandeCameraDroite(ICommande):
    """Commande pour tourner la caméra à droite."""
    
    def __init__(self, servo):
        self.servo = servo
    
    def executer(self) -> dict:
        self.servo.tourner(0)
        return {}
    
    def get_nom(self) -> str:
        return "cam_droite"
