class EtatRobot:

    def __init__(self):
        self._etat = {
            "mode_detection": False,
            "mode_autonome": False,
            "action_courante": "stop",
            "debut_rotation": 0,
            "objet_cible": "person",
            "couleur_cible": None  # Couleur cible pour la détection (ex: "rouge", "bleu")
        }
    
    def __getattr__(self, name: str):
        if name in self._etat:
            return self._etat[name]
        raise AttributeError(f"EtatRobot n'a pas d'attribut '{name}'")
    
    def __setattr__(self, name: str, value):
        if name == "_etat":
            super().__setattr__(name, value)
        else:
            self._etat[name] = value
    
    def appliquer_changements(self, changements: dict):
        self._etat.update(changements)
