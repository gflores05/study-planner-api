from src.application.dtos.assessment import StartAssessmentResponseDTO
from src.application.ports.outbound.messaging.event_publisher import EventPublisherPort
from src.application.ports.outbound.repositories.assessment_repository import (
  AssessmentRepository,
)
from src.application.use_cases.assessment.error import (
  AssessmentInvalidInputError,
  AssessmentInvalidStatusError,
  AssessmentNotFoundError,
  AssessmentQuestionNotFoundError,
)
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.domain.assessment.problems import (
  AssessmentInvalidStatusProblem,
  AssessmentProblem,
  AssessmentQuestionNotFoundProblem,
)
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.util.date_util import utc_now


class StartAssessmentUseCaseAdapter(UseCaseEventPublisher):
  def __init__(
    self,
    assessment_repository: AssessmentRepository,
    event_publisher: EventPublisherPort,
  ):
    self.event_publisher = event_publisher
    self.assessment_repository = assessment_repository

  async def execute(self, id: str) -> StartAssessmentResponseDTO:
    assessment_id = AssessmentId.parse(id).unwrap_or_map_and_raise(
      lambda problem: AssessmentInvalidInputError(
        value=str(problem.value), field="assessment_id"
      )
    )

    assessment = (await self.assessment_repository.get(assessment_id)).get_or_raise(
      AssessmentNotFoundError(assessment_id=id)
    )

    assessment.start(started_on=utc_now()).unwrap_or_map_and_raise(map_error)

    await self.assessment_repository.save(assessment=assessment)

    await self._publish_events(assessment)

    return StartAssessmentResponseDTO(assessment_id=str(assessment.id))


def map_error(problem: AssessmentProblem):
  match problem:
    case AssessmentInvalidStatusProblem():
      return AssessmentInvalidStatusError(
        assessment_id=problem.assessment_id,
        current_status=problem.current_status,
        required_status=problem.required_status,
      )
    case AssessmentQuestionNotFoundProblem():
      return AssessmentQuestionNotFoundError(
        assessment_id=problem.assessment_id, question_id=problem.question_id
      )
