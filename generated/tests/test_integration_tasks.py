import pytest
from generated.src.tasks import Statut, Tache, InterfaceUtilisateur

def test_creer_et_lister_taches():
    interface = InterfaceUtilisateur()
    interface.creer_tache("Test 1", "Description 1")
    interface.creer_tache("Test 2", "Description 2")
    taches = interface.lister_taches()
    assert len(taches) == 2
    assert taches[0].titre == "Test 1"
    assert taches[1].titre == "Test 2"

def test_mettre_a_jour_et_obtenir_tache():
    interface = InterfaceUtilisateur()
    interface.creer_tache("Test")
    tache = interface.mettre_a_jour_tache(0, titre="Nouveau Titre", statut=Statut.TERMINE)
    assert tache.titre == "Nouveau Titre"
    assert tache.statut == Statut.TERMINE
    tache_obtenu = interface.obtenir_tache(0)
    assert tache_obtenu.titre == "Nouveau Titre"
    assert tache_obtenu.statut == Statut.TERMINE

def test_supprimer_et_lister_taches():
    interface = InterfaceUtilisateur()
    interface.creer_tache("Test 1")
    interface.creer_tache("Test 2")
    interface.supprimer_tache(0)
    taches = interface.lister_taches()
    assert len(taches) == 1
    assert taches[0].titre == "Test 2"