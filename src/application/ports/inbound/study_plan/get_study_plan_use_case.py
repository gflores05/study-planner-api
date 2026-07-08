from typing import Protocol

from src.application.dtos.study_plan import (
  StudyPlanDTO,
)


class GetStudyPlanUseCasePort(Protocol):
  async def execute(self, id: str) -> StudyPlanDTO: ...
