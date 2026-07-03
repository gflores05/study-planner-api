from src.application.dtos.assessment import AssessmentDTO
from src.application.mappers.assessment_mapper import map_assessment_domain_to_dto
from src.application.ports.outbound.messaging.event_publisher import EventPublisherPort
from src.application.ports.outbound.repositories.assessment_repository import (
  AssessmentRepository,
)
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.util.date_util import utc_now


class CompleteAssessmentUseCase(UseCaseEventPublisher):
  def __init__(
    self,
    event_publisher: EventPublisherPort,
    assessment_repository: AssessmentRepository,
  ):
    super().__init__(event_publisher)
    self.assessment_repository = assessment_repository

  async def execute(self, id: str) -> AssessmentDTO:
    assessment_id = AssessmentId.parse(id).unwrap_or_raise()

    assessment = (await self.assessment_repository.get(assessment_id)).get_or_raise(
      ValueError("AssessmentNotFound")
    )

    assessment.complete(completed_on=utc_now())

    await self.assessment_repository.save(assessment=assessment)

    await self._publish_events(assessment)

    return map_assessment_domain_to_dto(assessment)
