from src.application.dtos.assessment import AssessmentDTO
from src.application.mappers.assessment_mapper import map_assessment_domain_to_dto
from src.application.ports.outbound.repositories.assessment_repository import (
  AssessmentRepository,
)
from src.domain.assessment.value_objects.assessment_id import AssessmentId


class GetAssessmentUseCase:
  def __init__(self, assessment_repository: AssessmentRepository):
    self.assessment_repository = assessment_repository

  async def execute(self, id: str) -> AssessmentDTO:
    assessment_id = AssessmentId.parse(id).unwrap_or_raise()

    assessment = (await self.assessment_repository.get(assessment_id)).get_or_raise(
      ValueError("AssessmentNotFound")
    )

    return map_assessment_domain_to_dto(assessment)
