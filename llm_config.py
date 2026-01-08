import os

from dotenv import load_dotenv
from langchain_mistralai.chat_models import ChatMistralAI

load_dotenv()


def make_mistral_llm(model: str = "mistral-small-latest") -> ChatMistralAI:
    """
    Fabrique un client ChatMistralAI prêt à l'emploi.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY manquant dans l'environnement /.env")

    return ChatMistralAI(model_name=model)
