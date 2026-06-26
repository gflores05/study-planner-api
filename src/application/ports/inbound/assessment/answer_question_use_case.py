from typing import Protocol

from src.application.dtos.assessment import AnswerQuestionRequestDTO
from src.application.dtos.question import QuestionDTO


class AnswerQuestionUseCase(Protocol):
  async def execute(self, dto: AnswerQuestionRequestDTO) -> QuestionDTO: ...
