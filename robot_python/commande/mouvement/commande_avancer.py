from commande.interfaces.i_commande import ICommande


class CommandeAvancer(ICommande):
    
    def __init__(self, navigation):
        self.navigation = navigation
    
    def executer(self) -> dict:
        self.navigation.avancer()
        return {"action_courante": "avancer"}
