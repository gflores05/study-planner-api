import uuid

from src.domain.answer.answer import Answer
from src.domain.answer.value_objects.answer_id import AnswerId
from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.domain.question.question import Question
from src.domain.question.value_objects.question_id import QuestionId
from src.domain.question.value_objects.question_text import QuestionText
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.infrastructure.adapters.outbound.persistence.models.question_model import (
  AnswerModel,
  QuestionModel,
)
from src.shared.option import Option


def map_question_model_to_domain(model: QuestionModel) -> Question:
  return Question.reconstitute(
    id=QuestionId.parse(str(model.id)).unwrap_or_raise(),
    created_on=model.created_on,
    modified_on=model.modified_on,
    version=model.version,
    text=QuestionText.parse(model.text).unwrap_or_raise(),
    options=[map_answer_model_to_domain(o) for o in model.options],
    answer=AnswerOption.parse(model.answer).unwrap_or_raise(),
    selected_answer=Option.of(
      AnswerOption.parse(model.selected_answer).unwrap_or_raise()
      if model.selected_answer is not None
      else None
    ),
    assessment_id=AssessmentId.parse(str(model.assessment_id)).unwrap_or_raise(),
  )


def map_answer_model_to_domain(model: AnswerModel) -> Answer:
  return Answer.reconstitute(
    id=AnswerId.parse(model.id).unwrap_or_raise(),
    text=NonEmptyString.parse(model.text).unwrap_or_raise(),
    option=AnswerOption.parse(model.option).unwrap_or_raise(),
  )


def map_question_domain_to_model(domain: Question) -> QuestionModel:
  return QuestionModel(
    id=uuid.UUID(str(domain.id)),
    created_on=domain.created_on,
    modified_on=domain.modified_on,
    version=domain.version,
    text=str(domain.text),
    options=[map_answer_domain_to_model(a) for a in domain.options],
    answer=str(domain.answer),
    selected_answer=str(domain.selected_answer.get())
    if domain.selected_answer.is_some
    else None,
    assessment_id=str(domain.assessment_id),
  )


def map_answer_domain_to_model(domain: Answer) -> AnswerModel:
  return AnswerModel(
    id=str(domain.id), text=str(domain.text), option=str(domain.option)
  )
