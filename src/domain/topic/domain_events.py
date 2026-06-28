from dataclasses import dataclass
from datetime import datetime

from src.domain.assessment.assessment import Assessment
from src.domain.sub_topic.sub_topic import SubTopic
from src.shared.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class TopicSubTopicsAdded(DomainEvent):
  event_name: str = "TopicSubTopicsAdded"
  sub_topics: list[SubTopic]
  generated_on: datetime


@dataclass(frozen=True, kw_only=True)
class TopicAssessmentAdded(DomainEvent):
  event_name: str = "TopicAssessmentAdded"
  assessment: Assessment
  generated_on: datetime
