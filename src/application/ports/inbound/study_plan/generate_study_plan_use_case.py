from typing import Protocol

from src.application.dtos.study_plan import (
  GenerateStudyPlanDTO,
  StudyPlanResponseDTO,
)


class GenerateStudyPlanUseCasePort(Protocol):
  async def execute(self, dto: GenerateStudyPlanDTO) -> StudyPlanResponseDTO: ...
