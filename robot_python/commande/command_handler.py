import time

class CommandHandler:
    
    def __init__(self, navigation, servo):
        self.nav = navigation
        self.servo = servo
        self._commandes = {
            "avancer": lambda: (self.nav.avancer(), {"action_courante": "avancer"})[1],
            "reculer": lambda: (self.nav.reculer(), {"action_courante": "reculer"})[1],
            "gauche": lambda: (self.nav.tourner_gauche(), {"action_courante": "tourner_gauche_90", "debut_rotation": time.time()})[1],
            "droite": lambda: (self.nav.tourner_droite(), {"action_courante": "tourner_droite_90", "debut_rotation": time.time()})[1],
            "stop": lambda: (self.nav.arreter(), {"action_courante": "stop", "mode_autonome": False})[1],
            
            "cam_gauche": lambda: (self.servo.tourner(180), {})[1],
            "cam_droite": lambda: (self.servo.tourner(0), {})[1],
            "cam_centre": lambda: (self.servo.tourner(90), {})[1],
            
            "detect_on": lambda: {"mode_detection": True},
            "detect_off": lambda: {"mode_detection": False},
            "auto_on": lambda: {"mode_autonome": True},
            "auto_off": lambda: (self.nav.arreter(), {"mode_autonome": False})[1],
        }
    
    def executer_commande(self, commande_texte: str) -> dict:
        print(f"[BLE] Commande reçue : {commande_texte}")
        
        if "set_object" in commande_texte:
            try:
                _, new_target = commande_texte.split(":")
                objet_cible = new_target.strip()
                print(f"Nouvelle cible de détection : {objet_cible}")
                return {"objet_cible": objet_cible}
            except ValueError:
                print("Erreur format set_object. Attendu: set_object:classe")
                return {}
        
        for cle, commande in self._commandes.items():
            if cle in commande_texte:
                return commande()
        
        print(f"Commande inconnue : {commande_texte}")
        return {}
    
    def lister_commandes(self) -> list:
        return list(self._commandes.keys())
