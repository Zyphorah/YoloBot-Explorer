from commande.interfaces.i_commande import ICommande


class CommandeDetectionOn(ICommande):
    
    def executer(self) -> dict:
        print("Mode Détection ACTIVÉ")
        return {"mode_detection": True}
