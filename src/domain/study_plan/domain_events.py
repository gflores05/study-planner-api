from dataclasses import dataclass, field
from datetime import datetime

from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.shared.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class StudyPlanTopicsAdded(DomainEvent):
  event_name: str = field(default="StudyPlanTopicsAdded")
  generated_on: datetime
  study_plan_id: StudyPlanId


@dataclass(frozen=True, kw_only=True)
class StudyPlanRequested(DomainEvent):
  event_name: str = field(default="StudyPlanRequested")
  study_plan_id: StudyPlanId
  requested_on: datetime
