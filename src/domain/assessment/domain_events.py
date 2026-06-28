from dataclasses import dataclass, field
from datetime import datetime

from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.domain.question.question import Question
from src.shared.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class AssessmentCompleted(DomainEvent):
  assessment_id: AssessmentId
  completed_on: datetime
  event_name: str = field(default="AssessmentCompleted")


@dataclass(frozen=True, kw_only=True)
class AssessmentStarted(DomainEvent):
  assessment_id: AssessmentId
  started_on: datetime
  event_name: str = field(default="AssessmentStarted")


@dataclass(frozen=True, kw_only=True)
class AssessmentAddQuestions(DomainEvent):
  assessment_id: AssessmentId
  generated_on: datetime
  questions: list[Question]
  event_name: str = field(default="AssessmentAddQuestions")
