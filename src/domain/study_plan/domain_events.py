from dataclasses import dataclass, field
from datetime import datetime

from src.shared.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class StudyPlanGenerated(DomainEvent):
  event_name: str = field(default="StudyPlanGenerated")
  generated_on: datetime
  study_plan_id: str
  generated_by_user_id: str


@dataclass(frozen=True, kw_only=True)
class StudyPlanErrorReported(DomainEvent):
  event_name: str = field(default="StudyPlanErrorReported")
  failed_on: datetime
  study_plan_id: str
  reported_by_user_id: str
  error: str


@dataclass(frozen=True, kw_only=True)
class StudyPlanRequested(DomainEvent):
  event_name: str = field(default="StudyPlanRequested")
  study_plan_id: str
  requested_by_user_id: str
  requested_on: datetime
