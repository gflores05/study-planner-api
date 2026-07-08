from dataclasses import dataclass
from datetime import datetime

from src.domain.answer.answer import Answer
from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.domain.question.domain_events import AnswerSelected
from src.domain.question.value_objects.question_id import QuestionId
from src.domain.question.value_objects.question_text import QuestionText
from src.shared.aggregate_root import AggregateRoot
from src.shared.option import Option


@dataclass(kw_only=True)
class Question(AggregateRoot[QuestionId]):
  text: QuestionText
  options: list[Answer]
  answer: AnswerOption
  selected_answer: Option[AnswerOption]
  assessment_id: AssessmentId

  @staticmethod
  def create(
    text: QuestionText,
    options: list[Answer],
    answer: AnswerOption,
    assessment_id: AssessmentId,
  ) -> "Question":
    return Question(
      id=QuestionId.create(),
      text=text,
      options=options,
      answer=answer,
      selected_answer=Option.nothing(),
      assessment_id=assessment_id,
    )

  @staticmethod
  def reconstitute(
    id: QuestionId,
    created_on: datetime,
    modified_on: datetime,
    version: int,
    text: QuestionText,
    options: list[Answer],
    answer: AnswerOption,
    selected_answer: Option[AnswerOption],
    assessment_id: AssessmentId,
  ) -> "Question":
    return Question(
      id=id,
      created_on=created_on,
      modified_on=modified_on,
      version=version,
      text=text,
      options=options,
      answer=answer,
      selected_answer=selected_answer,
      assessment_id=assessment_id,
    )

  @property
  def is_correct(self) -> bool:
    return self.selected_answer.is_some and self.selected_answer.get() == self.answer

  def select_answer(self, selected_answer: AnswerOption, answer_on: datetime):
    self.selected_answer = Option.some(selected_answer)
    self.modified_on = answer_on
    self.add_domain_event(
      AnswerSelected(
        question_id=str(self.id),
        selected_answer=str(selected_answer),
        answer_on=answer_on,
      )
    )
