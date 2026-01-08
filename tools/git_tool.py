# tools/git_tool.py

import subprocess
from langchain_core.tools import tool


@tool
def git_diff() -> str:
    """Affiche le diff Git courant (changes non commit)."""
    result = subprocess.run(["git", "diff"], text=True, capture_output=True)
    return result.stdout


@tool
def git_commit(message: str) -> str:
    """Effectue git add . puis git commit -m 'message'."""
    subprocess.run(["git", "add", "."], check=True)

    result = subprocess.run(
        ["git", "commit", "-m", message], text=True, capture_output=True
    )

    return result.stdout or result.stderr


@tool
def git_push(remote: str = "origin", branch: str = "main") -> str:
    """Effectue un git push vers le remote et la branche spécifiés."""
    result = subprocess.run(
        ["git", "push", remote, branch], text=True, capture_output=True
    )
    return result.stdout or result.stderr
