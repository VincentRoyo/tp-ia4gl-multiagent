from typing import List, Optional
from models import Tache, Statut
from service import TacheService


class TacheController:
    """
    Classe représentant le contrôleur de gestion des tâches.
    """
    def __init__(self):
        """
        Initialise une nouvelle instance du contrôleur de gestion des tâches.
        """
        self.service = TacheService()

    def creer_tache(self, titre: str, description: Optional[str] = None) -> Tache:
        """
        Crée une nouvelle tâche.
        """
        return self.service.creer_tache(titre, description)

    def lister_taches(self) -> List[Tache]:
        """
        Liste toutes les tâches.
        """
        return self.service.lister_taches()

    def obtenir_tache(self, index: int) -> Optional[Tache]:
        """
        Obtient une tâche par son index.
        """
        return self.service.obtenir_tache(index)

    def mettre_a_jour_tache(self, index: int, titre: Optional[str] = None, description: Optional[str] = None, statut: Optional[Statut] = None) -> Optional[Tache]:
        """
        Met à jour une tâche.
        """
        return self.service.mettre_a_jour_tache(index, titre, description, statut)

    def supprimer_tache(self, index: int) -> Optional[Tache]:
        """
        Supprime une tâche.
        """
        return self.service.supprimer_tache(index)
