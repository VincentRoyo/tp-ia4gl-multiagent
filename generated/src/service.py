from typing import List, Optional
from models import Tache, Statut
from repository import TacheRepository


class TacheService:
    """
    Classe représentant le service de gestion des tâches.
    """
    def __init__(self):
        """
        Initialise une nouvelle instance du service de gestion des tâches.
        """
        self.repository = TacheRepository()

    def creer_tache(self, titre: str, description: Optional[str] = None) -> Tache:
        """
        Crée une nouvelle tâche.
        """
        return self.repository.creer_tache(titre, description)

    def lister_taches(self) -> List[Tache]:
        """
        Liste toutes les tâches.
        """
        return self.repository.lister_taches()

    def obtenir_tache(self, index: int) -> Optional[Tache]:
        """
        Obtient une tâche par son index.
        """
        return self.repository.obtenir_tache(index)

    def mettre_a_jour_tache(self, index: int, titre: Optional[str] = None, description: Optional[str] = None, statut: Optional[Statut] = None) -> Optional[Tache]:
        """
        Met à jour une tâche.
        """
        return self.repository.mettre_a_jour_tache(index, titre, description, statut)

    def supprimer_tache(self, index: int) -> Optional[Tache]:
        """
        Supprime une tâche.
        """
        return self.repository.supprimer_tache(index)
