from commande.interfaces.i_commande import ICommande


class CommandeReculer(ICommande):
    """Commande pour faire reculer le robot."""
    
    def __init__(self, navigation):
        self.navigation = navigation
    
    def executer(self) -> dict:
        self.navigation.reculer()
        return {"action_courante": "reculer"}
    
    def get_nom(self) -> str:
        return "reculer"
