# tools/run_pytest_tool.py

import subprocess
from langchain_core.tools import tool


@tool
def run_pytest(path: str = "generated/tests") -> str:
    """
    Exécute pytest sur le chemin donné (par défaut generated/tests)
    et retourne exit code + stdout/stderr.
    """
    result = subprocess.run(["pytest", path, "-q"], text=True, capture_output=True)

    return (
        f"exit={result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
