from src.application.dtos.assessment import AssessmentDTO
from src.application.mappers.assessment_mapper import map_assessment_dto_to_domain
from src.application.ports.outbound.messaging.event_publisher import EventPublisher
from src.application.ports.outbound.repositories.assessment_repository import (
  AssessmentRepository,
)
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.util.date_util import utc_now


class CreateAssessmentUseCase(UseCaseEventPublisher):
  def __init__(
    self, assessment_repository: AssessmentRepository, event_publisher: EventPublisher
  ):
    self.assessment_repository = assessment_repository
    self.event_publisher = event_publisher

  async def execute(self, dto: AssessmentDTO) -> None:
    assessment = map_assessment_dto_to_domain(dto).unwrap_or_raise()

    assessment.add_questions(generated_on=utc_now())

    await self.assessment_repository.save(assessment=assessment)

    await self._publish_events(assessment)
