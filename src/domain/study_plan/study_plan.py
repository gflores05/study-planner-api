from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal

from src.domain.study_plan.domain_events import StudyPlanGenerated, StudyPlanRequested
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.study_plan.value_objects.subject import Subject
from src.domain.topic.topic import Topic
from src.domain.topic.value_objects.topic_title import TopicTitle
from src.shared.aggregate_root import AggregateRoot
from src.shared.result import Result, Unit


@dataclass
class AddTopicParams:
  title: TopicTitle


class StudyPlanError(Exception):
  pass


StudyPlanLevel = Literal[
  "Elementary School", "High School", "Preparatory", "University", "Postgraduate"
]


class StudyPlanStatus(Enum):
  PENDING = "PENDING"
  GENERATING = "GENERATING"
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

  def request(self, requested_on: datetime) -> Result[Unit, StudyPlanError]:
    if self.status != StudyPlanStatus.PENDING:
      return Result.fail(StudyPlanError("StudyPlanNotPending"))

    self.status = StudyPlanStatus.GENERATING

    self.add_domain_event(
      StudyPlanRequested(study_plan_id=self.id, requested_on=requested_on)
    )

    return Result.ok(Unit)

  def add_topic(self, params: AddTopicParams):
    topic = Topic.create(
      title=params.title,
      sub_topics=[],
      study_plan_id=self.id,
    )
    self.topics.append(topic)

    return topic

  def report_plan_generated(self, generated_on: datetime):
    self.modified_on = generated_on
    self.status = StudyPlanStatus.COMPLETED
    self.add_domain_event(
      StudyPlanGenerated(study_plan_id=self.id, generated_on=generated_on)
    )
