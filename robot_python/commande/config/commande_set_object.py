from commande.interfaces.i_commande import ICommande


class CommandeSetObject(ICommande):
    """Commande pour définir l'objet cible de détection."""
    
    def __init__(self, commande_texte: str):
        self.commande_texte = commande_texte
    
    def executer(self) -> dict:
        try:
            _, new_target = self.commande_texte.split(":")
            objet_cible = new_target.strip()
            print(f"Nouvelle cible de détection : {objet_cible}")
            return {"objet_cible": objet_cible}
        except ValueError:
            print("Erreur format set_object. Attendu: set_object:classe")
            return {}
    
    def get_nom(self) -> str:
        return "set_object"
