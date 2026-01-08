# tools/run_formatter_tool.py

import subprocess
from langchain_core.tools import tool


@tool
def run_formatter(path: str = ".") -> str:
    """Formate le code Python avec black sur le chemin donné."""
    result = subprocess.run(["black", path], text=True, capture_output=True)
    return result.stdout or result.stderr
