Feature: Gestion des tâches

  Scenario: Créer et lister des tâches
    Given une nouvelle interface utilisateur
    When je crée une tâche "Terminer le rapport" avec la description "Finir le rapport pour la réunion de demain"
    And je crée une tâche "Faire les courses" avec la description "Acheter du lait, des œufs et du pain"
    Then je devrais avoir 2 tâches dans la liste

  Scenario: Mettre à jour et supprimer des tâches
    Given une nouvelle interface utilisateur
    And je crée une tâche "Test"
    When je mets à jour la tâche 0 avec le statut "en cours"
    And je supprime la tâche 0
    Then je devrais avoir 0 tâches dans la liste

  Scenario: Vérifier le statut des tâches
    Given une nouvelle interface utilisateur
    And je crée une tâche "Test"
    When je mets à jour la tâche 0 avec le statut "terminé"
    Then la tâche 0 devrait avoir le statut "terminé"