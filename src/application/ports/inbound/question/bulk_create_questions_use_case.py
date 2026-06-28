from typing import Protocol

from src.application.dtos.question import QuestionDTO


class BulkCreateQuestionsUseCase(Protocol):
  async def execute(self, dtos: list[QuestionDTO]) -> None: ...
