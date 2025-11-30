class EtatRobot:

    def __init__(self):
        self._etat = {
            "mode_detection": True,
            "mode_autonome": True,
            "action_courante": "stop",
            "debut_rotation": 0,
            "objet_cible": "person"
        }
    
    def appliquer_changements(self, changements: dict):
        self._etat.update(changements)
    
    def obtenir(self, cle: str):
        return self._etat.get(cle)
    
    def definir(self, cle: str, valeur):
        self._etat[cle] = valeur
    
    @property
    def mode_detection(self) -> bool:
        return self._etat["mode_detection"]
    
    @property
    def mode_autonome(self) -> bool:
        return self._etat["mode_autonome"]
    
    @property
    def action_courante(self) -> str:
        return self._etat["action_courante"]
    
    @action_courante.setter
    def action_courante(self, valeur: str):
        self._etat["action_courante"] = valeur
    
    @property
    def debut_rotation(self) -> float:
        return self._etat["debut_rotation"]
    
    @property
    def objet_cible(self) -> str:
        return self._etat["objet_cible"]
    
    def __repr__(self) -> str:
        return f"EtatRobot({self._etat})"
