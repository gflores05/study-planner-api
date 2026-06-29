from src.application.dtos.question import QuestionDTO
from src.application.mappers.answer_mapper import (
  map_answer_domain_to_dto,
  map_answer_dto_to_domain,
)
from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.domain.question.question import Question
from src.domain.question.value_objects.question_text import QuestionText
from src.shared.result import Result
from src.shared.validation_error import ValidationError
from src.util.result_util import traverse


def map_question_dto_to_domain(dto: QuestionDTO) -> Result[Question, ValidationError]:
  return Result.ok(
    Question.create(
      text=QuestionText.parse(dto.text).unwrap_or_raise(),
      options=traverse(
        [map_answer_dto_to_domain(answerDTO) for answerDTO in dto.options]
      ).unwrap_or_raise(),
      answer=AnswerOption.parse(dto.answer).unwrap_or_raise(),
      assessment_id=AssessmentId.parse(dto.assessment_id).unwrap_or_raise(),
    )
  )


def map_question_domain_to_dto(domain: Question) -> QuestionDTO:
  return QuestionDTO(
    id=str(domain.id),
    text=str(domain.text),
    options=[map_answer_domain_to_dto(dto) for dto in domain.options],
    answer=str(domain.answer),
    selected_answer=str(domain.selected_answer.get())
    if domain.selected_answer.is_some
    else None,
    assessment_id=str(domain.assessment_id),
  )
