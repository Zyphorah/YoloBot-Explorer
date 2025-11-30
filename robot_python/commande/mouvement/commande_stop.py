from commande.interfaces.i_commande import ICommande


class CommandeStop(ICommande):
    """Commande pour arrêter le robot."""
    
    def __init__(self, navigation):
        self.navigation = navigation
    
    def executer(self) -> dict:
        self.navigation.arreter()
        return {
            "action_courante": "stop",
            "mode_autonome": False
        }
    
    def get_nom(self) -> str:
        return "stop"
