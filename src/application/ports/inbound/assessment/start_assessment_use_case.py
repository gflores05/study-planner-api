from typing import Protocol

from src.application.dtos.assessment import StartAssessmentResponseDTO


class StartAssessmentUseCase(Protocol):
  async def execute(self, id: str) -> StartAssessmentResponseDTO: ...
