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
    """
    Invocateur du patron Commande.
    Utilise un dictionnaire pour le mapping des commandes.
    """
    
    def __init__(self, navigation, servo):
        """
        Initialise le CommandHandler avec les dépendances nécessaires.
        
        Args:
            navigation: Instance de FacadeNavigation pour les commandes de mouvement
            servo: Instance de Servo pour les commandes de caméra
        """
        self.navigation = navigation
        self.servo = servo
        
        # Dictionnaire de mapping des commandes
        self._commandes: Dict[str, ICommande] = {}
        
        self._enregistrer_commandes()
    
    def _enregistrer_commandes(self):
        """Enregistre toutes les commandes dans le dictionnaire."""
        
        # Dictionnaire de toutes les commandes avec leur clé
        self._commandes = {
            # Commandes de mouvement
            "avancer": CommandeAvancer(self.navigation),
            "reculer": CommandeReculer(self.navigation),
            "gauche": CommandeTournerGauche(self.navigation),
            "droite": CommandeTournerDroite(self.navigation),
            "stop": CommandeStop(self.navigation),
            
            # Commandes servo caméra
            "cam_gauche": CommandeCameraGauche(self.servo),
            "cam_droite": CommandeCameraDroite(self.servo),
            "cam_centre": CommandeCameraCentre(self.servo),
            
            # Commandes de mode
            "detect_on": CommandeDetectionOn(),
            "detect_off": CommandeDetectionOff(),
            "auto_on": CommandeAutonomeOn(),
            "auto_off": CommandeAutonomeOff(self.navigation),
        }
    
    def executer_commande(self, commande_texte: str) -> dict:
        """
        Exécute une commande à partir de son texte en utilisant le dictionnaire.
        
        Args:
            commande_texte: Le texte de la commande reçue (ex: "avancer", "set_object:person")
            
        Returns:
            dict: Les changements d'état à appliquer
        """
        print(f"[BLE] Commande reçue : {commande_texte}")
        
        # Cas spécial pour set_object (commande avec paramètre)
        if "set_object" in commande_texte:
            cmd = CommandeSetObject(commande_texte)
            return cmd.executer()
        
        # Recherche dans le dictionnaire
        for cle, commande in self._commandes.items():
            if cle in commande_texte:
                return commande.executer()
        
        print(f"Commande inconnue : {commande_texte}")
        return {}
    
    def ajouter_commande(self, cle: str, commande: ICommande):
        """
        Ajoute une nouvelle commande au dictionnaire.
        
        Args:
            cle: La clé pour identifier la commande
            commande: Instance d'une commande implémentant ICommande
        """
        self._commandes[cle] = commande
    
    def supprimer_commande(self, cle: str) -> bool:
        """
        Supprime une commande du dictionnaire.
        
        Args:
            cle: La clé de la commande à supprimer
            
        Returns:
            bool: True si la commande a été supprimée, False sinon
        """
        if cle in self._commandes:
            del self._commandes[cle]
            return True
        return False
    
    def lister_commandes(self) -> List[str]:
        """Retourne la liste des clés de commandes disponibles."""
        return list(self._commandes.keys())
    
    def obtenir_commande(self, cle: str) -> ICommande:
        """
        Retourne une commande par sa clé.
        
        Args:
            cle: La clé de la commande
            
        Returns:
            ICommande ou None si non trouvée
        """
        return self._commandes.get(cle)
