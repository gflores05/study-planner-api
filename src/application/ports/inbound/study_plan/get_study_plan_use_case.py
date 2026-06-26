from typing import Protocol

from src.application.dtos.study_plan import (
  StudyPlanDTO,
)


class GetStudyPlanUseCase(Protocol):
  async def execute(self, id: str) -> StudyPlanDTO: ...
