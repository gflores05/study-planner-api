from typing import Protocol

from src.application.dtos.study_plan import (
  AddStudyPlanTopics,
  StudyPlanResponseDTO,
)


class AddTopicsUseCase(Protocol):
  async def execute(self, dto: AddStudyPlanTopics) -> StudyPlanResponseDTO: ...
