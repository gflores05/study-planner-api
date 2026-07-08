from typing import Protocol

from src.application.dtos.assessment import AnswerQuestionResponseDTO
from src.application.dtos.question import QuestionDTO


class AnswerQuestionUseCasePort(Protocol):
  async def execute(
    self, assessment_id: str, dto: AnswerQuestionResponseDTO
  ) -> QuestionDTO: ...
