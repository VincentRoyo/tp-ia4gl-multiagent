import pytest
from generated.src.models import Statut, Tache, InterfaceUtilisateur

def test_scenario_complet():
    interface = InterfaceUtilisateur()
    # Création de tâches
    tache1 = interface.creer_tache("Terminer le rapport", "Finir le rapport pour la réunion de demain")
    tache2 = interface.creer_tache("Faire les courses", "Acheter du lait, des œufs et du pain")
    
    # Vérification de la création des tâches
    assert len(interface.lister_taches()) == 2
    
    # Mise à jour de tâche
    interface.mettre_a_jour_tache(0, statut=Statut.EN_COURS)
    tache_mise_a_jour = interface.obtenir_tache(0)
    assert tache_mise_a_jour.statut == Statut.EN_COURS
    
    # Suppression de tâche
    interface.supprimer_tache(1)
    assert len(interface.lister_taches()) == 1
    
    # Vérification de la tâche restante
    tache_restante = interface.obtenir_tache(0)
    assert tache_restante.titre == "Terminer le rapport"
    assert tache_restante.statut == Statut.EN_COURS

