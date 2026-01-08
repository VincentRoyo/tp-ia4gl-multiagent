# main.py

from orchestrator.orchestrator import OrchestratorAgent


def main() -> None:
    print("\n================ MULTI-AGENT GL4IA ================\n")
    print("Entre ton objectif (user story, fonctionnalité, etc.)\n")

    user_goal = input("> ")

    if not user_goal.strip():
        print("Objectif vide. Fin.")
        return

    orchestrator = OrchestratorAgent()

    print("\n[1/5] Création de l'orchestrateur OK")
    print("[2/5] Envoi de l'objectif à l'orchestrateur…\n")

    result = orchestrator.run(user_goal)

    print("\n[3/5] Orchestration terminée")
    print("[4/5] Résultat final renvoyé par l'orchestrateur :\n")
    print(result)

    print("\n[5/5] Les artefacts générés sont disponibles dans : ./generated/\n")


if __name__ == "__main__":
    main()
