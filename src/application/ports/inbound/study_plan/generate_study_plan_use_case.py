from typing import Protocol

from src.application.dtos.study_plan import (
  GenerateStudyPlanRequestDTO,
  GenerateStudyPlanResponseDTO,
)


class GenerateStudyPlanUseCase(Protocol):
  async def execute(
    self, dto: GenerateStudyPlanRequestDTO
  ) -> GenerateStudyPlanResponseDTO: ...
