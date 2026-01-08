import pytest
from generated.src.tasks import Statut, Tache, InterfaceUtilisateur

def test_creer_tache():
    interface = InterfaceUtilisateur()
    tache = interface.creer_tache("Test", "Description de test")
    assert tache.titre == "Test"
    assert tache.description == "Description de test"
    assert tache.statut == Statut.A_FAIRE

def test_lister_taches():
    interface = InterfaceUtilisateur()
    interface.creer_tache("Test 1", "Description 1")
    interface.creer_tache("Test 2", "Description 2")
    taches = interface.lister_taches()
    assert len(taches) == 2

def test_obtenir_tache():
    interface = InterfaceUtilisateur()
    interface.creer_tache("Test")
    tache = interface.obtenir_tache(0)
    assert tache is not None
    assert tache.titre == "Test"

def test_mettre_a_jour_tache():
    interface = InterfaceUtilisateur()
    interface.creer_tache("Test")
    tache = interface.mettre_a_jour_tache(0, titre="Nouveau Titre", statut=Statut.TERMINE)
    assert tache.titre == "Nouveau Titre"
    assert tache.statut == Statut.TERMINE

def test_supprimer_tache():
    interface = InterfaceUtilisateur()
    interface.creer_tache("Test")
    tache = interface.supprimer_tache(0)
    assert tache is not None
    assert interface.obtenir_tache(0) is None
