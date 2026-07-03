from src.application.dtos.assessment import AnswerQuestionRequestDTO
from src.application.dtos.question import QuestionDTO
from src.application.mappers.question_mapper import map_question_domain_to_dto
from src.application.ports.outbound.messaging.event_publisher import EventPublisherPort
from src.application.ports.outbound.repositories.assessment_repository import (
  AssessmentRepository,
)
from src.application.ports.outbound.repositories.question_repository import (
  QuestionRepository,
)
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.domain.question.value_objects.question_id import QuestionId
from src.util.date_util import utc_now


class AnswerQuestionUseCase(UseCaseEventPublisher):
  def __init__(
    self,
    assessment_repository: AssessmentRepository,
    question_repository: QuestionRepository,
    event_publisher: EventPublisherPort,
  ):
    self.event_publisher = event_publisher
    self.assessment_repository = assessment_repository
    self.question_repository = question_repository

  async def execute(self, dto: AnswerQuestionRequestDTO) -> QuestionDTO:
    assessment_id = AssessmentId.parse(dto.assessment_id).unwrap_or_raise()

    assessment = (await self.assessment_repository.get(assessment_id)).get_or_raise(
      ValueError("AssessmentNotFound")
    )

    question_id = QuestionId.parse(dto.question_id).unwrap_or_raise()
    selected_answer = AnswerOption.parse(dto.selected_answer).unwrap_or_raise()

    question = assessment.answer_question(
      question_id=question_id, selected_answer=selected_answer, answer_on=utc_now()
    ).unwrap_or_raise()

    await self.assessment_repository.save(assessment=assessment)
    await self.question_repository.save(question=question)

    await self._publish_events(assessment)
    await self._publish_events(question)

    return map_question_domain_to_dto(question)
