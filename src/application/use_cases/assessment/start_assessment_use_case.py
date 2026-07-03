from src.application.dtos.assessment import StartAssessmentResponseDTO
from src.application.ports.outbound.messaging.event_publisher import EventPublisherPort
from src.application.ports.outbound.repositories.assessment_repository import (
  AssessmentRepository,
)
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.util.date_util import utc_now


class StartAssessmentUseCase(UseCaseEventPublisher):
  def __init__(
    self,
    assessment_repository: AssessmentRepository,
    event_publisher: EventPublisherPort,
  ):
    self.event_publisher = event_publisher
    self.assessment_repository = assessment_repository

  async def execute(self, id: str) -> StartAssessmentResponseDTO:
    assessment_id = AssessmentId.parse(id).unwrap_or_raise()

    assessment = (await self.assessment_repository.get(assessment_id)).get_or_raise(
      ValueError("AssessmentNotFound")
    )

    assessment.start(started_on=utc_now())

    await self.assessment_repository.save(assessment=assessment)

    await self._publish_events(assessment)

    return StartAssessmentResponseDTO(assessment_id=str(assessment.id))
