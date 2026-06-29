from typing import Protocol

from src.application.dtos.study_plan import (
  GeneratStudyPlanDTO,
)


class GenerateStudyPlanUseCase(Protocol):
  async def execute(self, dto: GeneratStudyPlanDTO) -> None: ...
