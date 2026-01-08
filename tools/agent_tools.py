# tools/agent_tools.py

from langchain_core.tools import tool

from agents.specs_agent import SpecsAgent
from agents.design_agent import DesignAgent
from agents.dev_agent import DevAgent
from agents.test_agent import TestAgent

from tools.run_formatter_tool import run_formatter
from tools.run_pytest_tool import run_pytest
from tools.git_tool import git_diff, git_commit
from tools.tools import read_file, write_file, list_files, append_to_memory_log

specs_agent = SpecsAgent(
    tools=[
        write_file,  # journalise : generated/specs.txt,
        append_to_memory_log
    ]
)

design_agent = DesignAgent(
    tools=[
        read_file,  # peut lire specs
        write_file,  # journalise design.txt
        list_files,
        append_to_memory_log
    ]
)

dev_agent = DevAgent(
    tools=[
        read_file,  # lit design/specs
        write_file,  # écrit code dans generated/src/
        list_files,
        run_formatter,  # black
        git_diff,
        git_commit,
        append_to_memory_log
    ]
)

test_agent = TestAgent(
    tools=[
        read_file,  # lit code
        write_file,  # écrit tests dans generated/tests/
        run_pytest,  # lance pytest sur generated/tests
        append_to_memory_log
    ]
)


@tool
def run_specs_agent(user_story: str) -> str:
    """Produit des spécifications détaillées à partir d'une user story."""
    return specs_agent.run(user_story)


@tool
def run_design_agent(input_text: str) -> str:
    """Produit un design logiciel à partir de specs et de besoins."""
    return design_agent.run(input_text)


@tool
def run_dev_agent(input_text: str) -> str:
    """Produit du code Python implémentant la fonctionnalité demandée."""
    return dev_agent.run(input_text)


@tool
def run_test_agent(input_text: str) -> str:
    """Produit des tests pytest vérifiant la fonctionnalité."""
    return test_agent.run(input_text)
