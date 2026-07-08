from dataclasses import dataclass, field
from datetime import datetime

from src.shared.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class AssessmentCompleted(DomainEvent):
  assessment_id: str
  completed_on: datetime
  event_name: str = field(default="AssessmentCompleted")


@dataclass(frozen=True, kw_only=True)
class AssessmentStarted(DomainEvent):
  assessment_id: str
  started_on: datetime
  event_name: str = field(default="AssessmentStarted")
