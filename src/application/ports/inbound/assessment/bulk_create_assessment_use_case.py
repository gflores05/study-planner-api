from typing import Protocol

from src.application.dtos.assessment import AssessmentDTO


class BulkCreateAssessmentUseCase(Protocol):
  async def execute(self, dtos: list[AssessmentDTO]) -> list[AssessmentDTO]: ...
