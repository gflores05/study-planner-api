from dataclasses import dataclass

from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.study_plan.value_objects.subject import Subject
from src.domain.topic.topic import Topic
from src.shared.aggregate_root import AggregateRoot


@dataclass(kw_only=True)
class StudyPlan(AggregateRoot[StudyPlanId]):
  subject: Subject
  topics: list[Topic]

  @staticmethod
  def create(subject: Subject, topics: list[Topic]) -> "StudyPlan":
    return StudyPlan(id=StudyPlanId.create(), subject=subject, topics=topics)

  @staticmethod
  def reconstitute(
    id: StudyPlanId, subject: Subject, topics: list[Topic]
  ) -> "StudyPlan":
    return StudyPlan(id=id, subject=subject, topics=topics)
