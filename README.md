# TP IA4GL – Système Multi‑Agent avec LangChain et MistralAI

Ce dépôt contient l’implémentation d’un **système multi‑agent** réalisé dans le cadre du TP *IA pour le Génie Logiciel / Introduction à l’architecture Agentic AI* (Master Génie Logiciel – Université de Montpellier).

L’objectif du projet est de mettre en œuvre une architecture **Agentic AI** capable d’automatiser et structurer plusieurs étapes du cycle de développement logiciel :
- analyse des besoins,
- conception logicielle,
- génération de code,
- génération et exécution de tests,
- orchestration et itérations.

Le système repose sur **LangChain** pour la gestion des agents et des tools, et sur le **LLM MistralAI** pour la génération des contenus.

---

## Architecture générale

Le projet est structuré autour de plusieurs agents spécialisés, coordonnés par un orchestrateur central :

- **SpecsAgent** : analyse de la user story et génération des spécifications fonctionnelles.
- **DesignAgent** : proposition d’une architecture et d’un design logiciel.
- **DevAgent** : génération du code Python à partir des spécifications et du design.
- **TestAgent** : génération et exécution des tests (unitaires, intégration, fonctionnels).
- **OrchestratorAgent** : découpage de l’objectif global, appel des agents dans le bon ordre, gestion des itérations.

Chaque agent est un agent LLM doté :
- d’un **contexte** définissant clairement son rôle,
- d’un ensemble de **tools LangChain** lui permettant d’agir sur le système (écriture de fichiers, exécution de tests, etc.).

---

## Arborescence du projet

```
tp-ia4gl-multiagent/
├── agents/
│   ├── base_agent.py
│   ├── specs_agent.py
│   ├── design_agent.py
│   ├── dev_agent.py
│   ├── test_agent.py
│   └── __init__.py
│
├── orchestrator/
│   ├── orchestrator.py
│   └── __init__.py
│
├── tools/
│   ├── tools.py
│   ├── agent_tools.py
│   ├── git_tool.py
│   ├── run_formatter_tool.py
│   ├── run_pytest_tool.py
│   └── __init__.py
│
├── generated/
│
├── llm_config.py
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

### Prérequis
- Python 3.14
- Git

### Étapes

```bash
git clone <url-du-repo>
cd tp-ia4gl-multiagent
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\Activate.ps1 sous Windows
pip install -r requirements.txt
```

---

## Configuration MistralAI

Définir la variable d’environnement dans un fichier .env à la racine du projet :

```bash
MISTRAL_API_KEY=VOTRE_CLE_API
```

---

## Lancement

```bash
python main.py
```

Saisir une user story en une ligne lorsque demandé.

---

## Auteurs

- Loris Bord
- Vincent Royo
