from typing import Protocol

from src.application.dtos.study_plan import (
  RequestStudyPlanDTO,
  StudyPlanResponseDTO,
)


class RequestStudyPlanUseCase(Protocol):
  async def execute(self, dto: RequestStudyPlanDTO) -> StudyPlanResponseDTO: ...
