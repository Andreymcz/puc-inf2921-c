from __future__ import annotations

import json
import os

import httpx

_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:8b")


def chat_completion(messages: list[dict], model: str = _MODEL) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
    }
    try:
        response = httpx.post(
            f"{_BASE_URL}/chat/completions",
            json=payload,
            timeout=120.0,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except httpx.ConnectError:
        raise RuntimeError(
            f"Ollama não está acessível em {_BASE_URL}. "
            "Verifique se o servidor Ollama está rodando."
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao chamar Ollama: {e}") from e
