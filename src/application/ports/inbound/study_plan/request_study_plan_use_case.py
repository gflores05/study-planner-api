from typing import Protocol

from src.application.dtos.study_plan import (
  RequestStudyPlanDTO,
  StudyPlanResponseDTO,
)


class RequestStudyPlanUseCasePort(Protocol):
  async def execute(self, dto: RequestStudyPlanDTO) -> StudyPlanResponseDTO: ...
