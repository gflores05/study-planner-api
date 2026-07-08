from src.application.dtos.assessment import (
  AnswerQuestionRequestDTO,
  AnswerQuestionResponseDTO,
)
from src.application.ports.outbound.messaging.event_publisher import EventPublisherPort
from src.application.ports.outbound.repositories.assessment_repository import (
  AssessmentRepository,
)
from src.application.ports.outbound.repositories.question_repository import (
  QuestionRepository,
)
from src.application.use_cases.assessment.error import (
  AssessmentError,
  AssessmentInvalidInputError,
  AssessmentInvalidStatusError,
  AssessmentNotFoundError,
  AssessmentQuestionNotFoundError,
  AssessmentUnknownError,
)
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.assessment.problems import (
  AssessmentInvalidStatusProblem,
  AssessmentProblem,
  AssessmentQuestionNotFoundProblem,
)
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.domain.question.value_objects.question_id import QuestionId
from src.util.date_util import utc_now


class AnswerQuestionUseCaseAdapter(UseCaseEventPublisher):
  def __init__(
    self,
    assessment_repository: AssessmentRepository,
    question_repository: QuestionRepository,
    event_publisher: EventPublisherPort,
  ):
    self.event_publisher = event_publisher
    self.assessment_repository = assessment_repository
    self.question_repository = question_repository

  async def execute(
    self, id: str, dto: AnswerQuestionRequestDTO
  ) -> AnswerQuestionResponseDTO:
    assessment_id = AssessmentId.parse(id).unwrap_or_map_and_raise(
      lambda problem: AssessmentInvalidInputError(
        value=str(problem.value), field="assessment_id"
      )
    )

    assessment = (await self.assessment_repository.get(assessment_id)).get_or_raise(
      AssessmentNotFoundError(assessment_id=id)
    )

    question_id = QuestionId.parse(dto.question_id).unwrap_or_map_and_raise(
      lambda problem: AssessmentInvalidInputError(
        value=str(problem.value), field="question_id"
      )
    )
    selected_answer = AnswerOption.parse(dto.selected_answer).unwrap_or_map_and_raise(
      lambda problem: AssessmentInvalidInputError(
        value=str(problem.value), field="selected_answer"
      )
    )

    question = assessment.answer_question(
      question_id=question_id, selected_answer=selected_answer, answer_on=utc_now()
    ).unwrap_or_map_and_raise(map_error)

    await self.assessment_repository.save(assessment=assessment)
    await self.question_repository.save(question=question)

    await self._publish_events(assessment)
    await self._publish_events(question)

    return AnswerQuestionResponseDTO(assessment_id=id, question_id=str(question.id))


def map_error(problem: AssessmentProblem) -> AssessmentError:
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
  return AssessmentUnknownError()
