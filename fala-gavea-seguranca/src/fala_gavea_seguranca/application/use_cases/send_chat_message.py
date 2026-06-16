from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from fala_gavea_seguranca.domain.entities.chat import ChatMessage
from fala_gavea_seguranca.domain.repositories.chat_repository import ChatMessageRepository
from fala_gavea_seguranca.infrastructure.llm.ollama_client import chat_completion
from fala_gavea_seguranca.infrastructure.vector_store.chroma_client import search, upsert_document

_SYSTEM_PROMPT = """Você é um assistente especializado em segurança pública na Gávea.
Responda com base nos relatos e investigações anteriores fornecidos como contexto.
Se não houver contexto suficiente, diga que não encontrou informações relevantes.
Responda sempre em português."""


@dataclass
class SendChatMessageInput:
    session_id: str
    user_text: str
    message_repo: ChatMessageRepository


class SendChatMessage:
    def execute(self, inp: SendChatMessageInput) -> tuple[ChatMessage, ChatMessage]:
        # Save user message first
        user_msg = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=inp.session_id,
            role="user",
            content=inp.user_text,
            created_at=datetime.now(tz=timezone.utc),
        )
        inp.message_repo.save(user_msg)

        # RAG: search both relatos and previous chats
        sources = search(inp.user_text, n_results=6)
        context_parts = []
        for hit in sources:
            m = hit["metadata"]
            prefix = "[relato]" if m.get("type") == "relato" else "[chat anterior]"
            context_parts.append(f"{prefix} {hit['text']}")

        context_block = "\n\n".join(context_parts) if context_parts else "Nenhum contexto encontrado."

        messages = [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Contexto:\n{context_block}\n\n"
                    f"Pergunta do delegado: {inp.user_text}"
                ),
            },
        ]

        answer = chat_completion(messages)

        assistant_msg = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=inp.session_id,
            role="assistant",
            content=answer,
            created_at=datetime.now(tz=timezone.utc),
            sources=sources,
        )
        inp.message_repo.save(assistant_msg)

        # Reindex the Q&A pair in ChromaDB so it enriches future searches
        try:
            qa_text = f"Pergunta: {inp.user_text}\nResposta: {answer}"
            upsert_document(
                doc_id=assistant_msg.id,
                text=qa_text,
                metadata={
                    "type": "chat",
                    "session_id": inp.session_id,
                    "lat": None,
                    "lon": None,
                    "category": "",
                    "status": "",
                },
            )
        except Exception:
            pass

        return user_msg, assistant_msg
