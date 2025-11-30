from commande.interfaces.i_commande import ICommande


class CommandeAvancer(ICommande):
    """Commande pour faire avancer le robot."""
    
    def __init__(self, navigation):
        self.navigation = navigation
    
    def executer(self) -> dict:
        self.navigation.avancer()
        return {"action_courante": "avancer"}
    
    def get_nom(self) -> str:
        return "avancer"
