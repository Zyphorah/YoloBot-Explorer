from commande.interfaces.i_commande import ICommande


class CommandeDetectionOff(ICommande):
    
    def executer(self) -> dict:
        print("Mode Détection DÉSACTIVÉ")
        return {"mode_detection": False}
    
    def get_nom(self) -> str:
        return "detect_off"
