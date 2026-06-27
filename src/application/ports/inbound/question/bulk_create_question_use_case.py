from typing import Protocol

from src.application.dtos.question import QuestionDTO


class BulkCreateQuestionUseCase(Protocol):
  async def execute(self, dtos: list[QuestionDTO]) -> list[QuestionDTO]: ...
