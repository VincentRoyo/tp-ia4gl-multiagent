from controller import TacheController
from models import Statut


def main() -> None:
    """
    Exemple d'utilisation du contrôleur de gestion des tâches.
    """
    controller = TacheController()
    
    # Création de tâches
    tache1 = controller.creer_tache("Terminer le rapport", "Finir le rapport pour la réunion de demain")
    tache2 = controller.creer_tache("Faire les courses", "Acheter du lait, des œufs et du pain")
    
    # Lister les tâches
    print("Tâches:")
    for tache in controller.lister_taches():
        print(f"- {tache.titre}: {tache.description} ({tache.statut.value})")
    
    # Mise à jour de tâche
    controller.mettre_a_jour_tache(0, statut=Statut.EN_COURS)
    
    # Suppression de tâche
    controller.supprimer_tache(1)
    
    # Lister les tâches après mise à jour et suppression
    print("\nTâches après mise à jour et suppression:")
    for tache in controller.lister_taches():
        print(f"- {tache.titre}: {tache.description} ({tache.statut.value})")


if __name__ == "__main__":
    main()