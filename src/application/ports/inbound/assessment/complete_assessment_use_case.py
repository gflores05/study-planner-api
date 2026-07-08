from typing import Protocol

from src.application.dtos.assessment import CompleteAssessmentResponseDTO


class CompleteAssessmentUseCasePort(Protocol):
  async def execute(self, id: str) -> CompleteAssessmentResponseDTO: ...
