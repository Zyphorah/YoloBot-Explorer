from commande.interfaces.i_commande import ICommande


class CommandeAutonomeOn(ICommande):
    
    def executer(self) -> dict:
        print("Mode Autonome ACTIVÉ")
        return {"mode_autonome": True}
