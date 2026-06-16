from __future__ import annotations

import json
from dataclasses import dataclass

from ...domain.entities.security_report import ReportCategory
from ...domain.exceptions import SecurityReportNotFoundError
from ...domain.repositories.security_report_repository import SecurityReportRepository
from ...infrastructure.ai.prompts import CATEGORIZE_PROMPT
from ...infrastructure.llm.ollama_client import chat_completion


@dataclass
class AutoCategorizeResult:
    category: str
    confidence: str
    justification: str


class AutoCategorizeReport:
    def __init__(self, repo: SecurityReportRepository) -> None:
        self._repo = repo

    def execute(self, id: str) -> AutoCategorizeResult:
        entity = self._repo.find_by_id(id)
        if entity is None:
            raise SecurityReportNotFoundError(id)

        prompt = CATEGORIZE_PROMPT.format(text=entity.text)
        raw = chat_completion([{"role": "user", "content": prompt}])

        try:
            data = json.loads(raw.strip())
            category_str = data["category"]
            category = ReportCategory(category_str)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(f"Resposta inválida do modelo: {raw!r}") from e

        self._repo.update_ai_suggested_category(id, category)

        return AutoCategorizeResult(
            category=category.value,
            confidence=data.get("confidence", ""),
            justification=data.get("justification", ""),
        )
