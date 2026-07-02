from dataclasses import dataclass

from src.domain.answer.value_objects.answer_id import AnswerId
from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.value_objects.non_empty_string import NonEmptyString


@dataclass(kw_only=True)
class Answer:
  id: AnswerId
  text: NonEmptyString
  option: AnswerOption

  @staticmethod
  def create(text: NonEmptyString, option: AnswerOption) -> "Answer":
    return Answer(id=AnswerId.create(), text=text, option=option)

  @staticmethod
  def reconstitute(
    id: AnswerId,
    text: NonEmptyString,
    option: AnswerOption,
  ) -> "Answer":
    return Answer(id=id, text=text, option=option)
