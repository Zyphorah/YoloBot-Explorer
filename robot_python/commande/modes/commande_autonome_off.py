from commande.interfaces.i_commande import ICommande


class CommandeAutonomeOff(ICommande):
    
    def __init__(self, navigation):
        self.navigation = navigation
    
    def executer(self) -> dict:
        self.navigation.arreter()
        print("Mode Autonome DÉSACTIVÉ")
        return {"mode_autonome": False}
