from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal

from src.domain.study_plan.domain_events import StudyPlanTopicsAdded
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.study_plan.value_objects.subject import Subject
from src.domain.topic.topic import Topic
from src.shared.aggregate_root import AggregateRoot

StudyPlanLevel = Literal[
  "Elementary School", "High School", "Preparatory", "University", "Postgraduate"
]


class StudyPlanStatus(Enum):
  PENDING = "PENDING"
  READY = "IN_PROGRESS"
  COMPLETED = "COMPLETED"


@dataclass(kw_only=True)
class StudyPlan(AggregateRoot[StudyPlanId]):
  subject: Subject
  level: StudyPlanLevel
  topics: list[Topic]
  status: StudyPlanStatus

  @staticmethod
  def create(subject: Subject, level: StudyPlanLevel) -> "StudyPlan":
    return StudyPlan(
      id=StudyPlanId.create(),
      subject=subject,
      topics=[],
      level=level,
      status=StudyPlanStatus.PENDING,
    )

  @staticmethod
  def reconstitute(
    id: StudyPlanId,
    subject: Subject,
    level: StudyPlanLevel,
    topics: list[Topic],
    status: StudyPlanStatus,
  ) -> "StudyPlan":
    return StudyPlan(id=id, subject=subject, level=level, topics=topics, status=status)

  def add_topics(self, topics: list[Topic], generated_on: datetime):
    self.topics = topics
    self.modified_on = generated_on

    self.add_domain_event(
      StudyPlanTopicsAdded(study_plan_id=self.id, generated_on=generated_on)
    )
