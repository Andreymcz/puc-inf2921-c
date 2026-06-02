from __future__ import annotations
import logging
import os
from openai import OpenAI

log = logging.getLogger(__name__)

OLLAMA_BASE_URL: str = os.getenv("GAVEALAB_OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL: str = os.getenv("GAVEALAB_OLLAMA_MODEL", "qwen2.5-coder:7b")


def get_client() -> OpenAI:
    """Return an OpenAI-compatible client pointed at the local Ollama instance."""
    return OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


def chat(messages: list[dict], model: str = OLLAMA_MODEL, temperature: float = 0.0) -> str:
    """Send messages to Ollama and return the text content of the first choice."""
    log.info("Calling Ollama model=%s url=%s msgs=%d", model, OLLAMA_BASE_URL, len(messages))
    for i, m in enumerate(messages):
        log.debug("  [%d] role=%s content_len=%d", i, m["role"], len(m.get("content", "")))
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        extra_body={"think": False},
    )
    content = response.choices[0].message.content
    log.info("Ollama response received: %d chars", len(content))
    log.debug("Raw response: %s", content[:500])
    return content
