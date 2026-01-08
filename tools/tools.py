from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_core.tools import tool

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "generated"
MEMORY = ROOT / "generated" / "memory"

def _safe_path(rel_path: str) -> Path:
    """
    Empêche d'écrire/lire en dehors de generated/.

    Accepte des chemins relatifs comme :
      - "specs.txt"
      - "src/models.py"
      - "tests/test_tasks.py"

    Tolère un préfixe "generated/" que l'on strippe.

    Refuse :
      - chemins absolus,
      - chemins avec '../'.
    """
    # Normalisation simple côté LLM
    rel_path = rel_path.replace("\\", "/").strip()

    # Tolérer un préfixe "generated/" : on le supprime
    if rel_path.startswith("generated/"):
        rel_path = rel_path[len("generated/"):]

    # Hard-block des patterns dangereux
    if rel_path.startswith("/") or rel_path.startswith("../") or "/../" in rel_path:
        raise ValueError(
            f"Chemin interdit pour write_file: {rel_path!r}. "
            "Donne un chemin RELATIF au dossier 'generated', "
            "sans '../' ni '/' au début."
        )

    # Path final
    p = (WORKSPACE / rel_path).resolve()

    # Normalisation Windows : virer le préfixe \\?\ si présent
    p_str = str(p)
    ws_str = str(WORKSPACE.resolve())

    if p_str.startswith("\\\\?\\"):
        p_str_cmp = p_str[4:]
    else:
        p_str_cmp = p_str

    if ws_str.startswith("\\\\?\\"):
        ws_str_cmp = ws_str[4:]
    else:
        ws_str_cmp = ws_str

    # Comparaison en lowercase pour être tranquille
    if not p_str_cmp.lower().startswith(ws_str_cmp.lower()):
        raise ValueError(
            f"Path traversal détecté: {p}\nSeul le dossier 'generated/' est autorisé."
        )

    return p



@tool
def list_files() -> List[str]:
    """Liste les fichiers dans generated/ (chemins relatifs)."""
    files: List[str] = []
    for path in WORKSPACE.rglob("*"):
        if path.is_file():
            files.append(str(path.relative_to(WORKSPACE)))
    return sorted(files)


@tool
def read_file(path: str) -> str:
    """Lit un fichier de generated/ et retourne son contenu."""
    p = _safe_path(path)
    if not p.exists():
        return f"[ERROR] File not found: {path}"
    return p.read_text(encoding="utf-8")


@tool
def write_file(path: str, content: str) -> str:
    """Écrit (ou remplace) un fichier dans generated/."""
    p = _safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"[OK] Wrote {path} ({len(content)} chars)"



def append_to_memory_log_raw(name: str, content: str) -> str:
    """
    Ajoute une entrée dans un fichier de log mémoire dans generated/memory/.
    (Version Python "raw", pour être appelée directement côté code.)
    """
    MEMORY.mkdir(parents=True, exist_ok=True)
    log_path = MEMORY / f"{name}.log"
    with log_path.open("a", encoding="utf-8") as f:
        f.write("\n\n=== ENTRY ===\n")
        f.write(content)
    return f"[OK] Appended to memory log {name}.log"


@tool
def append_to_memory_log(name: str, content: str) -> str:
    """
    Tool LangChain pour ajouter une entrée dans un fichier de log mémoire.

    À utiliser dans les tools des agents. Wrappe append_to_memory_log_raw.
    """
    return append_to_memory_log_raw(name, content)
