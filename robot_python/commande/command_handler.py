from typing import Dict, List
from commande.interfaces.i_commande import ICommande

# Imports des commandes depuis leurs modules respectifs
from commande.mouvement import (
    CommandeAvancer, CommandeReculer, CommandeTournerGauche,
    CommandeTournerDroite, CommandeStop
)
from commande.camera import (
    CommandeCameraGauche, CommandeCameraDroite, CommandeCameraCentre
)
from commande.modes import (
    CommandeDetectionOn, CommandeDetectionOff,
    CommandeAutonomeOn, CommandeAutonomeOff
)
from commande.config import CommandeSetObject


class CommandHandler:
    
    def __init__(self, navigation, servo):
        self.navigation = navigation
        self.servo = servo
        self._commandes: Dict[str, ICommande] = {}
        self._enregistrer_commandes()
    
    def _enregistrer_commandes(self):
        self._commandes = {
            "avancer": CommandeAvancer(self.navigation),
            "reculer": CommandeReculer(self.navigation),
            "gauche": CommandeTournerGauche(self.navigation),
            "droite": CommandeTournerDroite(self.navigation),
            "stop": CommandeStop(self.navigation),
            "cam_gauche": CommandeCameraGauche(self.servo),
            "cam_droite": CommandeCameraDroite(self.servo),
            "cam_centre": CommandeCameraCentre(self.servo),
            "detect_on": CommandeDetectionOn(),
            "detect_off": CommandeDetectionOff(),
            "auto_on": CommandeAutonomeOn(),
            "auto_off": CommandeAutonomeOff(self.navigation),
        }
    
    def executer_commande(self, commande_texte: str) -> dict:
        print(f"CommandHandler: commande recue: {commande_texte}")
        
        if "set_object" in commande_texte:
            cmd = CommandeSetObject(commande_texte)
            return cmd.executer()
        
        for cle, commande in self._commandes.items():
            if cle in commande_texte:
                return commande.executer()
        
        print(f"CommandHandler: commande inconnue: {commande_texte}")
        return {}
    
    def ajouter_commande(self, cle: str, commande: ICommande):
        self._commandes[cle] = commande
    
    def supprimer_commande(self, cle: str) -> bool:
        if cle in self._commandes:
            del self._commandes[cle]
            return True
        return False
    
    def lister_commandes(self) -> List[str]:
        return list(self._commandes.keys())
    
    def obtenir_commande(self, cle: str) -> ICommande:
        return self._commandes.get(cle)
