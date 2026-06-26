from dataclasses import dataclass
from typing import Literal

from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.study_plan.value_objects.subject import Subject
from src.domain.topic.topic import Topic
from src.shared.aggregate_root import AggregateRoot

StudyPlanLevel = Literal[
  "Elementary School", "High School", "Preparatory", "University", "Postgraduate"
]


@dataclass(kw_only=True)
class StudyPlan(AggregateRoot[StudyPlanId]):
  subject: Subject
  level: StudyPlanLevel
  topics: list[Topic]

  @staticmethod
  def create(
    subject: Subject, level: StudyPlanLevel, topics: list[Topic]
  ) -> "StudyPlan":
    return StudyPlan(
      id=StudyPlanId.create(), subject=subject, topics=topics, level=level
    )

  @staticmethod
  def reconstitute(
    id: StudyPlanId, subject: Subject, level: StudyPlanLevel, topics: list[Topic]
  ) -> "StudyPlan":
    return StudyPlan(id=id, subject=subject, level=level, topics=topics)
