from typing import Protocol

from src.application.dtos.assessment import AssessmentDTO


class CreateAssessmentUseCase(Protocol):
  async def execute(self, dtos: AssessmentDTO) -> None: ...
