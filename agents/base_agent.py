# agents/base_agent.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from langchain.agents import create_agent, AgentState
from langchain_core.tools import BaseTool

from llm_config import make_mistral_llm
from tools.tools import append_to_memory_log_raw
from pathlib import Path


class BaseAgent(ABC):
    """
    Agent de haut niveau, basé sur LangChain.

    - Chaque sous-classe définit :
      * un 'context' (rôle, format attendu, contraintes),
      * une liste de tools LangChain (BaseTool) qu'elle peut appeler.
    - En interne, BaseAgent construit un agent LangChain via create_agent(model, tools, system_prompt).
    - La méthode run(instructions: str) envoie les instructions utilisateur à cet agent.
    """

    def __init__(self, name: str, tools: Optional[List[BaseTool]] = None) -> None:
        self.name = name
        # LLM Mistral sous forme de ChatModel compatible LangChain
        self.llm = make_mistral_llm()
        # Copie défensive
        self.tools: List[BaseTool] = list(tools or [])

        # Graph LangChain interne (créé à la demande)
        self._lc_agent = None

    # ---- À définir dans chaque sous-classe ---------------------------------

    @property
    @abstractmethod
    def context(self) -> str:
        """
        Contexte statique de l'agent :
        - rôle,
        - structure de sortie,
        - contraintes.

        Exemple :
        "Tu es l'agent de spécification. Tu produis des user stories formelles..."
        """
        raise NotImplementedError

    # ---- Initialisation lazy de l’agent LangChain --------------------------

    def _ensure_agent(self) -> None:
        """
        Crée le graph LangChain (create_agent) une seule fois, au premier run.
        """
        if self._lc_agent is not None:
            return

        # Ici on utilise bien le paramètre 'model', pas 'llm'
        self._lc_agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.context,  # rôle / contraintes de l’agent
            name=self.name,
        )

    from pathlib import Path

    def _load_recent_memory(self, max_runs: int = 2, max_chars: int = 4000) -> str:
        """
        Charge les derniers 'max_runs' blocs de log pour cet agent depuis
        generated/memory/<AgentName>.log, basés sur le marqueur '=== RUN START ==='.

        - max_runs : nombre maximal de runs récents à inclure.
        - max_chars : garde au maximum ce nombre de caractères (par la fin) pour éviter
                      d'exploser le contexte.
        """
        try:
            root = Path(__file__).resolve().parents[1]
            mem_dir = root / "generated" / "memory"
            log_path = mem_dir / f"{self.name}.log"

            if not log_path.exists():
                return ""

            data = log_path.read_text(encoding="utf-8")

            marker = "=== RUN START ==="
            indices: list[int] = []

            # Trouver toutes les occurrences du marqueur
            start = 0
            while True:
                idx = data.find(marker, start)
                if idx == -1:
                    break
                indices.append(idx)
                start = idx + len(marker)

            if not indices:
                # pas de marqueur, on tombe back sur une simple fin de fichier tronquée
                if len(data) <= max_chars:
                    return data
                return data[-max_chars:]

            # On prend les max_runs derniers blocs
            selected_indices = indices[-max_runs:]
            # point de départ du plus ancien bloc retenu
            start_pos = selected_indices[0]
            recent = data[start_pos:]

            # On tronque si trop long
            if len(recent) > max_chars:
                return recent[-max_chars:]

            return recent

        except Exception:
            return ""

    # ---- API principale : exécuter l’agent ---------------------------------

    def run(self, instructions: str, *, verbose: bool = True) -> str:
        """
        Exécute l'agent sur des instructions texte et renvoie le dernier message.

        Utilise :
        - self.context : contexte statique de l'agent
        - _load_recent_memory() : mémoire courte à partir des logs
        - append_to_memory_log  : journalisation structuré de chaque run
        """

        if not isinstance(instructions, str) or not instructions.strip():
            raise ValueError(f"{self.name}.run : 'instructions' ne doit pas être vide.")

        # -------- LOG : démarrage --------
        if verbose:
            print(f"\n================= [{self.name}] =================")
            print("➡️  Démarrage de l'agent")
            print("➡️  Construction du prompt + envoi au modèle...\n")

        self._ensure_agent()

        # -------- Mémoire récente --------
        recent_memory = ""
        try:
            recent_memory = self._load_recent_memory()
        except Exception as e:
            if verbose:
                print(f"[{self.name}] ⚠️ Échec _load_recent_memory: {e}")

        if verbose:
            print(f"[{self.name}] ℹ️  Mémoire récente présente : {bool(recent_memory)}")

        # -------- Construction du prompt complet --------
        if recent_memory:
            full_input = (
                self.context.strip()
                + "\n\n=== Mémoire récente (historique condensé) ===\n"
                + recent_memory.strip()
                + "\n\n=== Nouvelle tâche à accomplir ===\n"
                + instructions.strip()
            )
        else:
            full_input = (
                self.context.strip()
                + "\n\n=== Nouvelle tâche à accomplir ===\n"
                + instructions.strip()
            )

        inputs = {
            "messages": [
                {
                    "role": "user",
                    "content": full_input,
                }
            ]
        }

        # -------- LOG : appel LangChain --------
        if verbose:
            print(f"[{self.name}] 🔁 Interaction LLM/tool en cours…")

        state: AgentState = self._lc_agent.invoke(inputs)

        # -------- LOG : réponse reçue --------
        if verbose:
            print(f"[{self.name}] ✅ retour du modèle reçu")
            print(f"[{self.name}] 📦 extraction du contenu final...")

        messages = state.get("messages", []) if isinstance(state, dict) else []

        final_text: str | None = None

        if messages:
            last = messages[-1]
            content = getattr(last, "content", "")

            if isinstance(content, str):
                final_text = content.strip()
            elif isinstance(content, list):
                final_text = "".join(
                    str(part.get("text", part)) if isinstance(part, dict) else str(part)
                    for part in content
                ).strip()
            else:
                final_text = str(content).strip()

        if not final_text:
            final_text = str(state)

        # -------- Mémoire automatique structurée --------
        try:
            log_block = (
                "=== RUN START ===\n"
                f"Agent: {self.name}\n"
                f"=== INSTRUCTIONS ===\n{instructions.strip()}\n\n"
                f"=== FULL_INPUT ===\n{full_input}\n\n"
                f"=== OUTPUT ===\n{final_text}\n"
                "=== RUN END ==="
            )
            append_to_memory_log_raw(
                name=self.name,
                content=log_block,
            )
        except Exception as e:
            if verbose:
                print(f"[{self.name}] ⚠️ Échec append_to_memory_log: {e}")

        if verbose:
            print(f"[{self.name}] 🟢 Terminé\n")

        return final_text

