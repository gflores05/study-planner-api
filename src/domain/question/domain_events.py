from dataclasses import dataclass, field
from datetime import datetime

from src.shared.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class AnswerSelected(DomainEvent):
  question_id: str
  selected_answer: str
  answer_on: datetime
  event_name: str = field(default="AnswerSelected")
