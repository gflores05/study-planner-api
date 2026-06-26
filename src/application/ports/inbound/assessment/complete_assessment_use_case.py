from typing import Protocol

from src.application.dtos.assessment import AssessmentDTO


class CompleteAssessmentUseCase(Protocol):
  async def execute(self, id: str) -> AssessmentDTO: ...
