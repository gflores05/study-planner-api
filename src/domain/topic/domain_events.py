from dataclasses import dataclass
from datetime import datetime

from src.domain.assessment.assessment import Assessment
from src.domain.topic.value_objects.topic_id import TopicId
from src.shared.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class TopicAssessmentGenerated(DomainEvent):
  event_name: str = "TopicAssessmentGenerated"
  topic_id: TopicId
  assessment: Assessment
  generated_on: datetime
