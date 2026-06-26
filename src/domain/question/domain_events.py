from dataclasses import dataclass, field
from datetime import datetime

from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.question.value_objects.question_id import QuestionId
from src.shared.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class AnswerSelected(DomainEvent):
  question_id: QuestionId
  selected_answer: AnswerOption
  answer_on: datetime
  event_name: str = field(default="AnswerSelected")
