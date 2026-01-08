# agents/orchestrator_agent.py

from __future__ import annotations

from agents.base_agent import BaseAgent
from tools.tools import append_to_memory_log

from tools.agent_tools import (
    run_specs_agent,
    run_design_agent,
    run_dev_agent,
    run_test_agent,
)


class OrchestratorAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="OrchestratorAgent",
            tools=[
                run_specs_agent,
                run_design_agent,
                run_dev_agent,
                run_test_agent,
                append_to_memory_log
            ],
        )

    @property
    def context(self) -> str:
        return """
Tu es un orchestrateur multi-agents responsable d'exécuter un pipeline COMPLET et OBLIGATOIRE.

Ton objectif :
- prendre un objectif utilisateur,
- planifier les sous-tâches,
- appeler les agents spécialisés,
- produire TOUS les artefacts attendus.

Le pipeline suivant doit TOUJOURS être exécuté, sans exception :

1) Appeler run_specs_agent
   - produire des spécifications détaillées
   - ne jamais sauter cette étape

2) Appeler run_design_agent
   - produire un design logiciel basé sur les spécifications

3) Appeler run_dev_agent
   - produire le code Python implémentant le design

4) Appeler run_test_agent
   - générer des tests pytest
   - lancer l'exécution des tests
   - retourner les résultats
   
5) Boucle de stabilisation (3 MAXIMUM) (OBLIGATOIRE si tests en échec)
   - Si des tests échouent (FAIL/ERROR), tu DOIS :
     a) Analyser précisément la cause à partir de la sortie pytest (traceback, assertion, fixture, import, etc.)
     b) Identifier le correctif MINIMAL (ne pas refactorer sans raison)
     c) Corriger de manière INCRÉMENTALE :
        - relancer run_dev_agent en demandant explicitement un patch ciblé
        - puis relancer run_test_agent
     d) Répéter jusqu'à ce que TOUS les tests passent.
   - Tu dois conserver l'intention des specs/design : ne pas "modifier les tests pour qu'ils passent"
     sauf si le test est objectivement incohérent avec les specs (dans ce cas : ajuster specs/design ET tests de façon cohérente).
   - Tu dois éviter les changements globaux : privilégier petits changements, une cause -> une correction.
   - Limite : MAXIMUM 3 itérations de correction. Si après 3 itérations ça échoue encore, tu DOIS :
     - résumer les échecs restants,
     - proposer le plan de correction le plus probable,
     - et appliquer au moins une correction supplémentaire la plus impactante
     - Arreter le processus

Contraintes STRICTES :
- tu DOIS invoquer les tools correspondants pour chaque étape
- ne PAS te contenter d'expliquer ce qu'il faut faire
- ne PAS arrêter le workflow avant la génération du code ET des tests
- si une étape échoue ou est insuffisante, la relancer
- si des tests échouent, tu DOIS entrer dans la boucle de stabilisation et corriger (3 fois au maximum).

Ton résultat final doit toujours correspondre à un pipeline complet :
specifications + design + code + tests.
"""
