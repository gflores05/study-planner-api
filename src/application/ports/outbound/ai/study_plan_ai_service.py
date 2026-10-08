from typing import Protocol

from src.application.dtos.study_plan import (
  StudyPlanAIGeneratedDTO,
  StudyPlanAIGenerationDTO,
)


class StudyPlanAIServicePort(Protocol):
  async def generate(
    self, params: StudyPlanAIGenerationDTO
  ) -> StudyPlanAIGeneratedDTO: ...
