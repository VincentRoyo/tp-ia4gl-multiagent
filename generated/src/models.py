from enum import Enum
from typing import Optional


class Statut(Enum):
    """
    Enumération des statuts possibles d'une tâche.
    """
    A_FAIRE = "à faire"
    EN_COURS = "en cours"
    TERMINE = "terminé"


class Tache:
    """
    Classe représentant une tâche.
    """
    def __init__(self, titre: str, description: Optional[str] = None, statut: Statut = Statut.A_FAIRE):
        """
        Initialise une nouvelle tâche.
        """
        self.titre = titre
        self.description = description
        self.statut = statut
