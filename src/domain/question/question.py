from dataclasses import dataclass

from src.domain.answer.answer import Answer
from src.domain.answer.value_objects.answer_option import AnswerOption
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

  @staticmethod
  def create(
    text: QuestionText, options: list[Answer], answer: AnswerOption
  ) -> "Question":
    return Question(
      id=QuestionId.create(),
      text=text,
      options=options,
      answer=answer,
      selected_answer=Option.nothing(),
    )

  @staticmethod
  def reconstitute(
    id: QuestionId, text: QuestionText, options: list[Answer], answer: AnswerOption
  ) -> "Question":
    return Question(
      id=id, text=text, options=options, answer=answer, selected_answer=Option.nothing()
    )

  @property
  def is_correct(self) -> bool:
    return self.selected_answer.is_some and self.selected_answer.get() == self.answer

  def select_answer(self, selected_answer: AnswerOption):
    self.selected_answer = Option.some(selected_answer)
    self.domain_events.append(
      AnswerSelected(question_id=self.id, selected_answer=selected_answer)
    )
