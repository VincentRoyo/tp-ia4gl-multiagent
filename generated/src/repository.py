from typing import List, Optional
from models import Tache, Statut


class TacheRepository:
    """
    Classe représentant le dépôt de tâches.
    """
    def __init__(self):
        """
        Initialise une nouvelle instance du dépôt de tâches.
        """
        self.taches: List[Tache] = []

    def creer_tache(self, titre: str, description: Optional[str] = None) -> Tache:
        """
        Crée une nouvelle tâche.
        """
        nouvelle_tache = Tache(titre, description)
        self.taches.append(nouvelle_tache)
        return nouvelle_tache

    def lister_taches(self) -> List[Tache]:
        """
        Liste toutes les tâches.
        """
        return self.taches

    def obtenir_tache(self, index: int) -> Optional[Tache]:
        """
        Obtient une tâche par son index.
        """
        if 0 <= index < len(self.taches):
            return self.taches[index]
        return None

    def mettre_a_jour_tache(self, index: int, titre: Optional[str] = None, description: Optional[str] = None, statut: Optional[Statut] = None) -> Optional[Tache]:
        """
        Met à jour une tâche.
        """
        tache = self.obtenir_tache(index)
        if tache:
            if titre:
                tache.titre = titre
            if description:
                tache.description = description
            if statut:
                tache.statut = statut
            return tache
        return None

    def supprimer_tache(self, index: int) -> Optional[Tache]:
        """
        Supprime une tâche.
        """
        if 0 <= index < len(self.taches):
            return self.taches.pop(index)
        return None
