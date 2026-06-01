from __future__ import annotations
import os
from openai import OpenAI

OLLAMA_BASE_URL: str = os.getenv("GAVEALAB_OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL: str = os.getenv("GAVEALAB_OLLAMA_MODEL", "qwen3:8b")


def get_client() -> OpenAI:
    """Return an OpenAI-compatible client pointed at the local Ollama instance."""
    return OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


def chat(messages: list[dict], model: str = OLLAMA_MODEL, temperature: float = 0.0) -> str:
    """Send messages to Ollama and return the text content of the first choice.

    Sets think=False to disable thinking mode for speed (matches tttc-poc behavior).
    """
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        extra_body={"think": False},
    )
    return response.choices[0].message.content
