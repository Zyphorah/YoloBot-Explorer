from commande.interfaces.i_commande import ICommande


class CommandeStop(ICommande):
    
    def __init__(self, navigation):
        self.navigation = navigation
    
    def executer(self) -> dict:
        self.navigation.arreter()
        return {
            "action_courante": "stop",
            "mode_autonome": False
        }
